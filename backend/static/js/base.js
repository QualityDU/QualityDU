document.addEventListener("DOMContentLoaded", function () {
    const toastElements = document.querySelectorAll('.toast');
    toastElements.forEach(function (toastElement) {
        const toast = new bootstrap.Toast(toastElement, { delay: 5000 });
        toast.show();
    });
});
