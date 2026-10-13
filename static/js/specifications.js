'use strict';
const addSpecification = document.getElementById('add-spec-row');
if (addSpecification) {
    addSpecification.addEventListener('click', (event) => {
        event.preventDefault();
        const total = document.getElementById('id_specifications-TOTAL_FORMS');
        const count = Number(total.value);
        if (count >= 50) return;
        const template = document.getElementById('specification-empty');
        const row = template.content.cloneNode(true);
        row.querySelectorAll('[name], [id], [for]').forEach((element) => {
            ['name', 'id', 'for'].forEach((attribute) => {
                if (element.hasAttribute(attribute)) element.setAttribute(attribute, element.getAttribute(attribute).replaceAll('__prefix__', String(count)));
            });
        });
        document.getElementById('specification-rows').appendChild(row);
        total.value = String(count + 1);
        document.getElementById(`id_specifications-${count}-attribute`).focus();
        addSpecification.disabled = count + 1 >= 50;
    });
}
