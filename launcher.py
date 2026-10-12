"""Arranque local y comandos: python launcher.py --help / InventariosAPP.exe --help."""
import argparse
import logging
import sqlite3
import sys
import webbrowser
from pathlib import Path

from config.version import __version__
from runtime_local import DataLock, configure_runtime, default_data_dir


def parser():
    result = argparse.ArgumentParser(description=f'InventariosAPP v{__version__} — uso local')
    result.add_argument('--version', action='version', version=f'v{__version__}')
    result.add_argument('--data-dir', type=Path, default=default_data_dir(), help='Carpeta persistente de datos')
    commands = result.add_subparsers(dest='command')
    server = commands.add_parser('serve', help='Iniciar Waitress exclusivamente en 127.0.0.1')
    server.add_argument('--port', type=int, default=8000)
    server.add_argument('--no-browser', action='store_true')
    commands.add_parser('init', help='Preparar una base nueva o migrar una existente sin borrar datos')
    manage = commands.add_parser('manage', help='Ejecutar un comando Django; por ejemplo createsuperuser')
    manage.add_argument('arguments', nargs=argparse.REMAINDER)
    backup = commands.add_parser('backup', help='Respaldar con la aplicación detenida')
    backup.add_argument('--output', type=Path)
    restore = commands.add_parser('restore', help='Restaurar un respaldo verificado, conservando el estado anterior')
    restore.add_argument('backup', type=Path)
    return result


def initialize_database():
    from django.conf import settings
    from django.core.management import call_command
    from django.db import connections
    from django.db.migrations.executor import MigrationExecutor
    from backups.backup_local import backup_project
    existing = Path(settings.DATABASES['default']['NAME']).exists()
    executor = MigrationExecutor(connections['default'])
    pending = executor.migration_plan(executor.loader.graph.leaf_nodes())
    if existing and pending:
        # Antes de modificar una base previamente creada, obtener una recuperación.
        connections.close_all()
        print(f'Respaldo previo a migraciones: {backup_project(settings.DATA_DIR)}', flush=True)
    call_command('migrate', interactive=False, verbosity=0)
    call_command('configure_inventory_roles', verbosity=0)
    print('Base preparada. No se eliminan registros existentes.', flush=True)


def main(argv=None):
    args = parser().parse_args(argv)
    if not args.command:
        args.command, args.port, args.no_browser = 'serve', 8000, False
    try:
        with DataLock(args.data_dir):
            if args.command == 'restore':
                from backups.backup_local import restore_backup
                root, previous = restore_backup(args.backup, args.data_dir, return_previous=True)
                print(f'Restaurado en: {root}', flush=True)
                if previous:
                    print(f'Estado anterior conservado en: {previous}', flush=True)
                return 0
            directory = configure_runtime(args.data_dir)
            import django
            django.setup()
            from django.db import connections
            if args.command == 'backup':
                from backups.backup_local import backup_project
                connections.close_all()
                print(f'Respaldo verificado: {backup_project(directory, args.output)}', flush=True)
            elif args.command == 'manage':
                if not args.arguments:
                    raise ValueError('Indica un comando Django, por ejemplo: manage createsuperuser')
                from django.core.management import execute_from_command_line
                execute_from_command_line(['InventariosAPP', *args.arguments])
            elif args.command == 'init':
                initialize_database()
            else:
                if not 1 <= args.port <= 65535:
                    raise ValueError('El puerto debe estar entre 1 y 65535.')
                initialize_database()
                from django.core.wsgi import get_wsgi_application
                from waitress import create_server
                from django.contrib.auth import get_user_model
                server = create_server(get_wsgi_application(), host='127.0.0.1', port=args.port, threads=4,
                                       max_request_body_size=25 * 1024 * 1024)
                print(f'InventariosAPP v{__version__} — http://127.0.0.1:{args.port}/search/', flush=True)
                print(f'Datos: {directory}. Detener: Ctrl+C en esta consola.', flush=True)
                if not get_user_model().objects.filter(is_superuser=True, is_active=True).exists():
                    print('No hay administrador. Detén la aplicación y ejecuta: manage createsuperuser', flush=True)
                if not args.no_browser:
                    webbrowser.open(f'http://127.0.0.1:{args.port}/accounts/login/')
                try:
                    server.run()
                finally:
                    server.close()
                    server.task_dispatcher.shutdown(timeout=60)
                    # Mantener el bloqueo hasta que terminen las escrituras activas.
                    with server.task_dispatcher.lock:
                        while server.task_dispatcher.threads:
                            server.task_dispatcher.thread_exit_cv.wait(1)
                    connections.close_all()
                    print('Aplicación detenida.', flush=True)
    except KeyboardInterrupt:
        print('Aplicación detenida.', flush=True)
    except (OSError, ValueError, RuntimeError, sqlite3.Error) as error:
        print(f'No se pudo completar la operación: {error}', file=sys.stderr, flush=True)
        return 1
    return 0


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    raise SystemExit(main())
