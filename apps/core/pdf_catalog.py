"""Tabla PDF del catálogo; sin servicios externos ni archivos temporales del usuario."""
from io import BytesIO
from pathlib import Path
from xml.sax.saxutils import escape

import reportlab
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, LongTable, TableStyle
from django.utils import timezone
from config.version import __version__

# Fuentes incluidas en ReportLab: acentos, µ y Ω sin depender de fuentes de Windows.
_fonts = Path(reportlab.__file__).parent / 'fonts'
pdfmetrics.registerFont(TTFont('InventorySans', str(_fonts / 'Vera.ttf')))
pdfmetrics.registerFont(TTFont('InventoryBold', str(_fonts / 'VeraBd.ttf')))


def build_catalog_pdf(components, filters):
    output = BytesIO()
    doc = SimpleDocTemplate(output, pagesize=landscape(A4), leftMargin=32, rightMargin=32,
                            topMargin=32, bottomMargin=40, title='InventariosAPP — Componentes',
                            author='InventariosAPP')
    body = ParagraphStyle('body', fontName='InventorySans', fontSize=8, leading=11, splitLongWords=True, textColor=colors.HexColor('#1e3445'))
    heading = ParagraphStyle('heading', parent=body, fontName='InventoryBold', fontSize=18, leading=22)
    header = ParagraphStyle('header', parent=body, fontName='InventoryBold', textColor=colors.white, alignment=1)

    def text(value, style=body):
        value = str(value if value is not None else '—')
        value = ''.join(char for char in value if ord(char) >= 32 or char == '\n')
        return Paragraph(escape(value).replace('\n', '<br/>'), style)

    timestamp = timezone.localtime().strftime('%d/%m/%Y %H:%M')
    story = [text('Componentes', heading), Spacer(1, 8),
             text(f'InventariosAPP v{__version__} · Generado: {timestamp} · Total: {len(components)}'), Spacer(1, 6)]
    descriptions = []
    if filters['q']:
        descriptions.append(f"Búsqueda: {filters['q']}")
    category_id = filters['selected_category']
    if category_id:
        from apps.components.models import Category
        category = Category.objects.filter(pk=category_id).first()
        descriptions.append(f'Categoría: {category.name if category else category_id}')
    if filters['availability']:
        descriptions.append({'available': 'Con existencias', 'empty': 'Sin existencias'}[filters['availability']])
    if filters['attention']:
        descriptions.append({'low': 'Existencias bajas', 'no_pdf': 'Sin ficha técnica', 'no_offer': 'Sin oferta'}[filters['attention']])
    descriptions.append('Orden: ' + {'name': 'Nombre', 'stock': 'Existencias ascendente', '-stock': 'Existencias descendente'}[filters['ordering']])
    story += [text(' · '.join(descriptions)), text('Componentes activos; incluye todas las páginas de los filtros aplicados.'), Spacer(1, 12)]
    if components:
        rows = [[text(label, header) for label in ('Referencia interna', 'Nombre', 'Categoría', 'Valor técnico', 'Parte del fabricante', 'Ubicación', 'Unidades')]]
        for component in components:
            stock = getattr(component, 'stock', None)
            rows.append([text(value) for value in (
                component.reference, component.name, component.category.name, component.value or '—',
                component.part_number or '—', str(component.location) if component.location else 'Sin asignar',
                stock.quantity if stock else 'Sin registro',
            )])
        table = LongTable(rows, colWidths=[doc.width * fraction for fraction in (.13, .22, .12, .12, .16, .15, .10)],
                          repeatRows=1, splitByRow=1, splitInRow=1, hAlign='LEFT')
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#17675a')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#eaf4f0')]),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), .4, colors.HexColor('#dce4e8')),
            ('LEFTPADDING', (0, 0), (-1, -1), 7), ('RIGHTPADDING', (0, 0), (-1, -1), 7),
            ('TOPPADDING', (0, 0), (-1, -1), 7), ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ]))
        story.append(table)
    else:
        story.append(text('No se encontraron componentes con los filtros aplicados.'))

    def footer(canvas, document):
        canvas.setFont('InventorySans', 8)
        canvas.setFillColor(colors.HexColor('#536677'))
        canvas.drawString(32, 20, f'InventariosAPP v{__version__} · {timestamp}')
        canvas.drawRightString(document.pagesize[0] - 32, 20, f'Página {document.page}')

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    return output.getvalue()
