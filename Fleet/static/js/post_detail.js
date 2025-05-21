/*
  Plik post_detail.js
  --------------------
  Obsługuje dynamiczne wypełnianie modali "Szczegóły", "Edycja" i "Usuń".
  - Po kliknięciu "Szczegóły" wypełnia dane w detailModal.
  - Po kliknięciu "Edytuj" zamyka "Szczegóły" i otwiera "Edycję".
  - Po kliknięciu "Usuń" otwiera modal potwierdzenia usunięcia.
  - Dynamicznie ustawia akcję formularza edycji.
*/

/**
 * Pobiera wartość z atrybutu data-* przycisku.
 * Jeśli atrybut nie istnieje, zwraca wartość domyślną.
 *
 * @param {HTMLElement} button - Przycisk z danymi
 * @param {string} attr - Nazwa atrybutu
 * @param {string} [fallback="Brak danych"] - Wartość domyślna
 * @returns {string} - Pobraną wartość lub fallback
 */
function getDataAttrOrFallback(button, attr, fallback = "Brak danych") {
    return button.getAttribute(attr) || fallback;
}

// 🔹 Pobieramy referencje do modali
var detailModal = document.getElementById('detailModal');
var editModal = document.getElementById('editModal');
var deleteModal = document.getElementById('deleteModal');
var deleteButton = document.getElementById('confirmDelete');
var postIdToDelete = null;

// 🔹 Obsługa modala "Szczegóły"
if (detailModal) {
    detailModal.addEventListener('show.bs.modal', function (event) {
        var button = event.relatedTarget;

        // Wypełnianie wartości modala szczegółów przejazdu
        document.getElementById('detail-title').textContent = getDataAttrOrFallback(button, 'data-title');
        document.getElementById('detail-content').textContent = getDataAttrOrFallback(button, 'data-content');
        document.getElementById('detail-create_at').textContent = getDataAttrOrFallback(button, 'data-create_at');
        document.getElementById('detail-author').textContent = getDataAttrOrFallback(button, 'data-author');
        document.getElementById('detail-distance').textContent = getDataAttrOrFallback(button, 'data-distance');
        document.getElementById('detail-start_location').textContent = getDataAttrOrFallback(button, 'data-start_location');
        document.getElementById('detail-end_location').textContent = getDataAttrOrFallback(button, 'data-end_location');
        document.getElementById('detail-travel_time').textContent = getDataAttrOrFallback(button, 'data-travel_time');
        document.getElementById('detail-vehicle').textContent = getDataAttrOrFallback(button, 'data-vehicle');

        // 🔹 Obsługa kliknięcia "Edytuj" → zamykamy modal szczegółów, otwieramy edycję
        var editLink = document.getElementById('editLink');
        if (editLink) {
            editLink.setAttribute('data-id', button.getAttribute('data-id'));
            editLink.addEventListener('click', function () {
                var modalInstance = bootstrap.Modal.getInstance(detailModal);
                modalInstance.hide();

                var editModalInstance = new bootstrap.Modal(editModal);
                editModalInstance.show();
            });
        }
    });
}

// 🔹 Obsługa modala "Usuń"
if (deleteModal) {
    deleteModal.addEventListener('show.bs.modal', function (event) {
        var button = event.relatedTarget;
        postIdToDelete = button.getAttribute('data-id');

        // Wstawienie tytułu do modala
        var modalTitle = deleteModal.querySelector('#postTitle');
        modalTitle.textContent = getDataAttrOrFallback(button, 'data-title');
    });

    // Pobieranie tokena CSRF do żądania POST
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Obsługa przycisku potwierdzającego usunięcie
    deleteButton.addEventListener('click', function () {
        fetch(`/posts/delete/${postIdToDelete}/`, {
            method: "POST", // 🔹 Zmieniono z DELETE na POST
            headers: {
                "X-CSRFToken": csrftoken,
                "X-Requested-With": "XMLHttpRequest",
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ post_id: postIdToDelete }) // 🔹 Wysyłamy ID w treści żądania
        }).then(response => {
            if (response.ok) {
                document.getElementById(`post-${postIdToDelete}`).remove();
                var modalInstance = bootstrap.Modal.getInstance(deleteModal);
                modalInstance.hide();
            } else {
                alert("Błąd: Nie udało się usunąć przejazdu!");
            }
        }).catch(error => {
            alert("Błąd połączenia z serwerem!");
        });
    });
}
