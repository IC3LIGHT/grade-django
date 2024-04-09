document.addEventListener("DOMContentLoaded", function() {
    var form = document.querySelector(".form-signin");
    form.noValidate = true;
    var registrationSuccess = false;
    var validationStarted = false;

    function clearErrors() {
        var errorMessages = document.querySelectorAll(".error-message");
        errorMessages.forEach(function(element) {
            element.textContent = '';
        });
    }

    function sendData(isFinalSubmit = false) {
        clearErrors();
        var formData = new FormData(form);
        formData.append("isFinalSubmit", isFinalSubmit);

        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/register/", true);
        xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");

        var csrfToken = form.querySelector('[name="csrfmiddlewaretoken"]').value;
        xhr.setRequestHeader("X-CSRFToken", csrfToken);

        xhr.onload = function() {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                if (response.success && isFinalSubmit) {
                    registrationSuccess = true;
                    window.location.href = "/auth/";
                } else if (!response.success) {
                    registrationSuccess = false;
                    Object.keys(response.errors).forEach(function(key) {
                        var errorContainer = document.getElementById("error-" + key);
                        var errors = response.errors[key].map(error => error.message).join(", ");
                        if (errorContainer) {
                            errorContainer.textContent = errors;
                        } else {
                            console.log("Проверить ошибки: " + key);
                        }
                    });
                }
            } else {
                alert("Произошла ошибка на сервере. Попробуйте позже.");
            }
        };

        xhr.send(formData);
    }

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        if (!registrationSuccess) {
            sendData(true);
        }
        if (!validationStarted) {
            validationStarted = true;
            form.addEventListener('input', function() {
                sendData(false);
            });
        }
    });
});
