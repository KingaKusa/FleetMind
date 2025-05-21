var detailModal = document.getElementById('detailModal');
var editModal = document.getElementById('editModal');
var deleteModal = document.getElementById('deleteModal');
var deleteButton = document.getElementById('confirmDelete');
var postIdToDelete = null;

// 🔹 Obsługa modala "Szczegóły"
if (detailModal) {
    detailModal.addEventListener('show.bs.modal', function (event) {
        var button = event.relatedTarget;

        document.getElementById('detail-title').textContent = button.getAttribute('data-title');
        document.getElementById('detail-content').textContent = button.getAttribute('data-content');
        document.getElementById('detail-create_at').textContent = button.getAttribute('data-create_at');
        document.getElementById('detail-author').textContent = button.getAttribute('data-author');

        var editLink = document.getElementById('editLink');
        if (editLink) {
            editLink.setAttribute('data-id', button.getAttribute('data-id'));
        }
    });
}

// 🔹 Obsługa zamykania modala "Szczegóły"
$('#detailModal').on('hidden.bs.modal', function () {
    $('body').removeClass('modal-open');
    $('.modal-backdrop').remove();
});

// 🔹 Obsługa modala "Usuń"
if (deleteModal) {
    deleteModal.addEventListener('show.bs.modal', function (event) {
        var button = event.relatedTarget;
        postIdToDelete = button.getAttribute('data-id');
    });
}
