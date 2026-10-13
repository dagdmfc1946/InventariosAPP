/* Mejoras progresivas: el guardado y la validación siguen en Django. */
(() => {
  'use strict';
  document.querySelectorAll('img[src*="/admin/img/icon-yes"][alt="True"]').forEach(image => image.alt = 'Sí');
  document.querySelectorAll('img[src*="/admin/img/icon-no"][alt="False"]').forEach(image => image.alt = 'No');
  document.querySelectorAll('.table-wrap, #changelist .results').forEach(region => {
    region.setAttribute('tabindex', '0');
    region.setAttribute('role', 'region');
    region.setAttribute('aria-label', region.querySelector('caption')?.textContent.trim() || 'Tabla de datos; desplázate para ver todas las columnas');
  });
  document.querySelectorAll('.field, .form-row').forEach((field, index) => {
    const input = field.querySelector('input:not([type="hidden"]), select, textarea');
    if (!input || !input.id) return;
    const describedBy = new Set((input.getAttribute('aria-describedby') || '').split(/\s+/).filter(Boolean));
    field.querySelectorAll('.help, .field-errors').forEach((help, helpIndex) => {
      if (!help.textContent.trim()) return;
      if (!help.id) help.id = `ui-help-${index}-${helpIndex}`;
      describedBy.add(help.id);
      if (help.classList.contains('field-errors')) input.setAttribute('aria-invalid', 'true');
    });
    const nativeErrors = field.querySelector('.errorlist');
    if (nativeErrors?.textContent.trim()) {
      if (!nativeErrors.id) nativeErrors.id = `ui-errors-${index}`;
      describedBy.add(nativeErrors.id);
      input.setAttribute('aria-invalid', 'true');
    }
    if (describedBy.size) input.setAttribute('aria-describedby', [...describedBy].join(' '));
  });

  document.querySelectorAll('input[type="password"]').forEach(input => {
    if (input.disabled || !input.id) return;
    const wrapper = document.createElement('div');
    wrapper.className = 'password-control';
    input.before(wrapper);
    wrapper.append(input);
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'password-toggle';
    button.textContent = 'Mostrar';
    button.setAttribute('aria-controls', input.id);
    button.setAttribute('aria-pressed', 'false');
    const label = document.querySelector(`label[for="${CSS.escape(input.id)}"]`);
    const fieldName = (label?.textContent || 'contraseña').trim().replace(/:$/, '').toLocaleLowerCase('es');
    button.setAttribute('aria-label', `Mostrar ${fieldName}`);
    button.addEventListener('click', () => {
      const show = input.type === 'password';
      input.type = show ? 'text' : 'password';
      button.textContent = show ? 'Ocultar' : 'Mostrar';
      button.setAttribute('aria-label', `${show ? 'Ocultar' : 'Mostrar'} ${fieldName}`);
      button.setAttribute('aria-pressed', String(show));
    });
    wrapper.append(button);
  });

  let firstSummary = null;
  document.querySelectorAll('form').forEach(form => {
    const invalidFields = [...form.querySelectorAll('.field, .form-row')].filter(field => field.querySelector('.field-errors, .errorlist')?.textContent.trim());
    if (!invalidFields.length) return;
    let summary = form.querySelector('.notice.error, .errornote');
    if (!summary) {
      summary = document.createElement('div');
      summary.className = 'notice error';
      const title = document.createElement('strong');
      title.textContent = 'Revisa los campos indicados.';
      summary.append(title);
      form.prepend(summary);
    }
    summary.setAttribute('role', 'alert');
    summary.setAttribute('tabindex', '-1');
    const list = document.createElement('ul');
    invalidFields.forEach(field => {
      const input = field.querySelector('input:not([type="hidden"]), select, textarea');
      if (!input?.id) return;
      const item = document.createElement('li');
      const link = document.createElement('a');
      link.href = `#${input.id}`;
      const errors = field.querySelector('.field-errors, .errorlist');
      const messages = [...errors.querySelectorAll('li')].map(item => item.textContent.trim());
      link.textContent = `${field.querySelector('label')?.textContent.trim() || 'Campo'}: ${messages.length ? messages.join(' ') : errors.textContent.trim()}`;
      link.addEventListener('click', () => input.focus());
      item.append(link);
      list.append(item);
    });
    summary.append(list);
    firstSummary ||= summary;
  });
  if (firstSummary) firstSummary.focus();
})();
