// Funkcja pomocnicza: pobiera dane z atrybutu data-* lub zwraca tekst domyślny (gdy brak danych)
function getDataAttrOrFallback(button, attr, fallback = "Brak danych") {
    const val = button.getAttribute(attr);
    return val ? val : fallback;
}

// Nasłuchujemy na otwarcie modala detailModal
var detailModal = document.getElementById('detailModal');

if(detailModal) {
    detailModal.addEventListener('show.bs.modal', function (event) {
        var button = event.relatedTarget;

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
