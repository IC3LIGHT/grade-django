document.addEventListener("DOMContentLoaded", function() {
    var form = document.querySelector(".form-auth");
    form.noValidate = true;
    var validationStarted = false;

    function validateFormData() {
        var formData = new FormData(form);
        formData.append("validateOnly", "true");
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/auth/", true);
        xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
        xhr.onload = function() {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                if (!response.success) {
                    displayErrors(response.errors);
                } else {
                    clearErrors();
                }
            } else {
                console.error("Ошибка валидации на сервере");
            }
        };
        xhr.send(formData);
    }

    function displayErrors(errors) {
        clearErrors();
        Object.keys(errors).forEach(function(key) {
            var errorContainer = document.getElementById("error-" + key);
            var errorsList = errors[key].map(error => error.message).join(", ");
            if (errorContainer) {errorContainer.textContent = errorsList;}
        });
    }

    function clearErrors() {
        var errorMessages = document.querySelectorAll(".error-message");
        errorMessages.forEach(function(element) {element.textContent = '';});
    }

    form.addEventListener("submit", function(e) {
        e.preventDefault();
        var formData = new FormData(form);
        formData.delete("validateOnly");
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/auth/", true);
        xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
        xhr.onload = function() {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                if (response.success) {window.location.href = "/";}
                else {
                    displayErrors(response.errors);
                }
            } else {alert("Произошла ошибка на сервере. Попробуйте позже.");}
        };
        xhr.send(formData);

        if (!validationStarted) {
            validationStarted = true;
            Array.from(form.elements).forEach(function(element) {
                element.addEventListener("input", validateFormData);
            });
        }
    });
});
