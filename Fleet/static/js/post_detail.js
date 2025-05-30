var detailModal = document.getElementById("detailModal");
var editModal = document.getElementById("editModal");
var deleteModal = document.getElementById("deleteModal");
var deleteButton = document.getElementById("confirmDelete");
var postIdToDelete = null;

// 🔹 Obsługa modala "Szczegóły"
if (!detailModal) {
    console.error("❌ Błąd: `detailModal` nie został znaleziony!");
} else {
    detailModal.addEventListener("show.bs.modal", function (event) {
        var button = event.relatedTarget;
        if (!button) {
            console.error("❌ Błąd: event.relatedTarget jest NULL!");
            return;
        }

        console.log("🔍 Otwieramy modal szczegółów...");
        document.getElementById("detail-title").textContent = button.getAttribute("data-title") || "Brak danych";
        document.getElementById("detail-content").textContent = button.getAttribute("data-content") || "Brak treści";
        document.getElementById("detail-create_at").textContent = button.getAttribute("data-create_at") || "Brak daty";
        document.getElementById("detail-author").textContent = button.getAttribute("data-author") || "Nieznany autor";
        document.getElementById("detail-distance").textContent = button.getAttribute("data-distance") || "Brak wartości";
        document.getElementById("detail-start_location").textContent = button.getAttribute("data-start_location") || "Nieokreślona";
        document.getElementById("detail-end_location").textContent = button.getAttribute("data-end_location") || "Nieokreślona";
        document.getElementById("detail-travel_time").textContent = button.getAttribute("data-travel_time") || "Brak czasu";
        document.getElementById("detail-vehicle").textContent = button.getAttribute("data-vehicle") || "Nieznany pojazd";

        var editLink = document.getElementById("editLink");
        if (editLink) {
            editLink.href = `/update_post/${button.getAttribute("data-id")}`;
        }
    });
}

// 🔹 Obsługa zamykania modala "Szczegóły"
$("#detailModal").on("hidden.bs.modal", function () {
    $("body").removeClass("modal-open");
    $(".modal-backdrop").remove();
});

// 🔹 Obsługa modala "Usuń"
if (deleteModal) {
    deleteModal.addEventListener("show.bs.modal", function (event) {
        var button = event.relatedTarget;
        postIdToDelete = button.getAttribute("data-id");
    });
}

// 🔹 Obsługa modala "Edytuj"
document.getElementById("editLink").addEventListener("click", function (event) {
    event.preventDefault(); // Zapobiegamy przekierowaniu linka

    var editModalElement = document.getElementById("editModal");

    if (!editModalElement) {
        console.error("❌ Błąd: `editModal` nie istnieje w momencie kliknięcia!");
        return;
    }

    console.log("✅ `editModal` znaleziony! Próba inicjalizacji...");

    try {
        var editModalInstance = new bootstrap.Modal(editModalElement);
        editModalInstance.show();
        console.log("✅ `editModal` poprawnie otwarty!");
    } catch (error) {
        console.error("❌ Błąd podczas inicjalizacji `editModal`: ", error);
    }
});

// 🔹 Sprawdzenie poprawnej inicjalizacji modali na starcie
document.addEventListener("DOMContentLoaded", function () {
    console.log("🔍 Sprawdzamy poprawność inicjalizacji modali...");

    var editModalElement = document.getElementById("editModal");
    var deleteModalElement = document.getElementById("deleteModal");

    if (!editModalElement || !deleteModalElement) {
        console.error("❌ Błąd: Jeden z modalów nie został znaleziony!");
    } else {
        console.log("✅ Modale poprawnie znalezione!");
        new bootstrap.Modal(editModalElement);
        new bootstrap.Modal(deleteModalElement);
    }
});
