document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('#existing-thumbnails-container .form-control').forEach(function(input) {
        input.disabled = false;
    });
});