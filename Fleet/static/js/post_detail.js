/*
  Plik post_detail.js
  --------------------
  Odpowiedzialny za dynamiczne wypełnianie modala szczegółów przejazdu.
  Funkcja getDataAttrOrFallback pobiera wartości z atrybutów data-* elementu wywołującego modal.
  Następnie, przy zdarzeniu "show.bs.modal", zawartość modala jest aktualizowana na podstawie tych wartości.
  Umieść ten plik w folderze static/js.
*/

/**
 * getDataAttrOrFallback
 * -----------------------
 * Pomocnicza funkcja służąca do pobrania wartości atrybutu data-* z danego elementu.
 * Jeśli atrybut nie istnieje lub jest pusty, funkcja zwraca wartość fallback.
 *
 * @param {HTMLElement} button - Element, z którego pobieramy wartość atrybutu.
 * @param {string} attr - Nazwa atrybutu (np. 'data-title').
 * @param {string} [fallback="Brak danych"] - Wartość domyślna zwracana, gdy atrybut jest pusty.
 * @returns {string} - Wartość atrybutu lub fallback.
 */
function getDataAttrOrFallback(button, attr, fallback = "Brak danych") {
    const val = button.getAttribute(attr);
    return val ? val : fallback;
}

// Pobieramy referencję do modala szczegółów przejazdu, który powinien mieć ID "detailModal".
// Dzięki temu możemy później dynamicznie uzupełnić jego zawartość.
var detailModal = document.getElementById('detailModal');

// Sprawdzamy, czy modal został poprawnie załadowany, aby uniknąć błędów
// w sytuacji, gdy modal nie jest obecny na stronie.
if (detailModal) {
    // Nasłuchujemy zdarzenia "show.bs.modal", które jest wywoływane tuż przed otwarciem modala.
    detailModal.addEventListener('show.bs.modal', function (event) {
        // event.relatedTarget to element (np. przycisk), który wywołał modal.
        var button = event.relatedTarget;

        // Aktualizujemy zawartość modala, pobierając dane z atrybutów data-* przycisku.
        // Dla każdego elementu modala (np. <span> o danym ID) przypisujemy odpowiednią wartość.
        document.getElementById('detail-title').textContent         = getDataAttrOrFallback(button, 'data-title');
        document.getElementById('detail-content').textContent       = getDataAttrOrFallback(button, 'data-content');
        document.getElementById('detail-create_at').textContent     = getDataAttrOrFallback(button, 'data-create_at');
        document.getElementById('detail-author').textContent        = getDataAttrOrFallback(button, 'data-author');
        document.getElementById('detail-distance').textContent      = getDataAttrOrFallback(button, 'data-distance');
        document.getElementById('detail-start_location').textContent  = getDataAttrOrFallback(button, 'data-start_location');
        document.getElementById('detail-end_location').textContent    = getDataAttrOrFallback(button, 'data-end_location');
        document.getElementById('detail-travel_time').textContent     = getDataAttrOrFallback(button, 'data-travel_time');
        document.getElementById('detail-vehicle').textContent         = getDataAttrOrFallback(button, 'data-vehicle');
    });
}
