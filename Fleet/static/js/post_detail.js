/*
  Plik post_detail.js
  --------------------
  Obsługuje dynamiczne wypełnianie modali "Szczegóły" i "Edycja".
  - Po kliknięciu "Szczegóły" wypełnia dane w detailModal.
  - Po kliknięciu "Edytuj" zamyka "Szczegóły" i otwiera "Edycję".
  - Dynamicznie ustawia akcję formularza edycji.
*/

/**
 * Pobiera wartość z atrybutu data-* przycisku
 * @param {HTMLElement} button - Przycisk z danymi
 * @param {string} attr - Nazwa atrybutu
 * @param {string} [fallback="Brak danych"] - Wartość domyślna
 * @returns {string} - Pobraną wartość lub fallback
 */
function getDataAttrOrFallback(button, attr, fallback = "Brak danych") {
    const val = button.getAttribute(attr);
    return val ? val : fallback;
}

// Pobieramy referencje do modali
var detailModal = document.getElementById('detailModal');
var editModal = document.getElementById('editModal');
var editLink = document.getElementById('editLink');

// Sprawdzamy, czy modal szczegółów istnieje
if (detailModal) {
    detailModal.addEventListener('show.bs.modal', function (event) {
        var button = event.relatedTarget;

        // Wypełnienie modala szczegółów
        document.getElementById('detail-title').textContent = getDataAttrOrFallback(button, 'data-title');
        document.getElementById('detail-content').textContent = getDataAttrOrFallback(button, 'data-content');
        document.getElementById('detail-create_at').textContent = getDataAttrOrFallback(button, 'data-create_at');
        document.getElementById('detail-author').textContent = getDataAttrOrFallback(button, 'data-author');
        document.getElementById('detail-distance').textContent = getDataAttrOrFallback(button, 'data-distance');
        document.getElementById('detail-start_location').textContent = getDataAttrOrFallback(button, 'data-start_location');
        document.getElementById('detail-end_location').textContent = getDataAttrOrFallback(button, 'data-end_location');
        document.getElementById('detail-travel_time').textContent = getDataAttrOrFallback(button, 'data-travel_time');
        document.getElementById('detail-vehicle').textContent = getDataAttrOrFallback(button, 'data-vehicle');

        // Przekazujemy ID przejazdu do przycisku "Edytuj"
        if (editLink) {
            editLink.setAttribute('data-id', button.getAttribute('data-id'));
        }
    });
}

// 🔹 Zamykamy modal szczegółów i otwieramy edycję
if (editLink) {
    editLink.addEventListener('click', function () {
        var modalInstance = bootstrap.Modal.getInstance(detailModal);
        if (modalInstance) {
            modalInstance.hide(); // Zamykamy "Szczegóły"
        }

        var editModalInstance = new bootstrap.Modal(editModal);
        editModalInstance.show(); // Otwieramy "Edycja"
    });
}

// Sprawdzamy, czy modal edycji istnieje
if (editModal) {
    editModal.addEventListener('show.bs.modal', function (event) {
        var button = document.querySelector(`[data-id="${editLink.getAttribute('data-id')}"]`);

        // Wypełnienie modala edycji
        document.getElementById('edit-title').value = getDataAttrOrFallback(button, 'data-title');
        document.getElementById('edit-content').value = getDataAttrOrFallback(button, 'data-content');
        document.getElementById('edit-distance').value = getDataAttrOrFallback(button, 'data-distance');
        document.getElementById('edit-start_location').value = getDataAttrOrFallback(button, 'data-start_location');
        document.getElementById('edit-end_location').value = getDataAttrOrFallback(button, 'data-end_location');
        document.getElementById('edit-travel_time').value = getDataAttrOrFallback(button, 'data-travel_time');
        document.getElementById('edit-vehicle').value = getDataAttrOrFallback(button, 'data-vehicle');

        // Ustawienie dynamicznej akcji formularza
        var editForm = document.getElementById('editPostForm');
        if (editForm) {
            editForm.setAttribute('action', `/posts/update/${editLink.getAttribute('data-id')}/`);
        }
    });
}
