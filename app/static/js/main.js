/**
 * Agricultural Crop Production Analysis System - Client JavaScript
 */

document.addEventListener("DOMContentLoaded", function () {
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll(".alert-dismissible");
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) {
                bsAlert.close();
            }
        }, 5000);
    });

    // File input filename display on upload page
    const fileInput = document.getElementById("csvFileInput");
    const fileLabel = document.getElementById("fileChosenLabel");
    if (fileInput && fileLabel) {
        fileInput.addEventListener("change", function () {
            if (fileInput.files.length > 0) {
                fileLabel.textContent = "Selected: " + fileInput.files[0].name;
                fileLabel.classList.remove("text-muted");
                fileLabel.classList.add("text-success", "fw-bold");
            } else {
                fileLabel.textContent = "No file chosen yet";
                fileLabel.classList.remove("text-success", "fw-bold");
                fileLabel.classList.add("text-muted");
            }
        });
    }
});
