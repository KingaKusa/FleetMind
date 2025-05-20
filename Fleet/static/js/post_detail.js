/*
  Plik post_detail.js jest odpowiedzialny za dynamiczne wypełnianie danych w modalu szczegółów przejazdu.
  Umieść ten plik w folderze static/js.
*/

/**
 * Pomocnicza funkcja getDataAttrOrFallback
 * Pobiera wartość z atrybutu data-* elementu przycisku.
 * Jeśli atrybut nie istnieje lub jest pusty, zwraca wartość domyślną (fallback).
 *
 * @param {HTMLElement} button - Element, z którego pobieramy dany atrybut.
 * @param {string} attr - Nazwa atrybutu (np. 'data-title').
 * @param {string} [fallback="Brak danych"] - Wartość domyślna, jeśli atrybut jest pusty.
 * @return {string} - Wartość atrybutu lub fallback.
 */
function getDataAttrOrFallback(button, attr, fallback = "Brak danych") {
    const val = button.getAttribute(attr);
    return val ? val : fallback;
}

// Pobieramy referencję do modala szczegółów (detailModal)
var detailModal = document.getElementById('detailModal');

// Jeśli modal istnieje (zapobiega błędom, gdy plik jest ładowany na stronie bez modala)
if (detailModal) {
    // Nasłuchiwanie zdarzenia "show.bs.modal", wywoływanego przy otwarciu modala
    detailModal.addEventListener('show.bs.modal', function (event) {
        // event.relatedTarget to przycisk, który wywołał modal
        var button = event.relatedTarget;

        // Aktualizacja zawartości modala – dla każdego elementu (span) pobieramy odpowiedni atrybut data-*
        document.getElementById('detail-title').textContent = getDataAttrOrFallback(button, 'data-title');
        document.getElementById('detail-content').textContent = getDataAttrOrFallback(button, 'data-content');
        document.getElementById('detail-create_at').textContent = getDataAttrOrFallback(button, 'data-create_at');
        document.getElementById('detail-author').textContent = getDataAttrOrFallback(button, 'data-author');
        document.getElementById('detail-distance').textContent = getDataAttrOrFallback(button, 'data-distance');
        document.getElementById('detail-start_location').textContent = getDataAttrOrFallback(button, 'data-start_location');
        document.getElementById('detail-end_location').textContent = getDataAttrOrFallback(button, 'data-end_location');
        document.getElementById('detail-travel_time').textContent = getDataAttrOrFallback(button, 'data-travel_time');
        document.getElementById('detail-vehicle').textContent = getDataAttrOrFallback(button, 'data-vehicle');
    });
}
