document.addEventListener('DOMContentLoaded', function() {
    var form = document.querySelector('.album-form');
    form.noValidate = true;
    var formSubmitted = false;

    function isFormValid() {
        return Array.from(form.elements).every(function(element) {
            return element.checkValidity();
        });
    }

    function clearErrors() {
        var errorMessages = document.querySelectorAll(".error-message");
        errorMessages.forEach(function(element) {
            element.textContent = '';
        });
    }

    function sendData() {
        var formData = new FormData(form);
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/albums/add_album/", true);
        xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");

        xhr.onload = function() {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                if (response.success) {
                    window.location.href = "/";
                } else {
                    if (formSubmitted) {
                        clearErrors();
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
                }
            } else {
                alert("Произошла ошибка на сервере, проверьте корректность загружаемых файлов");
            }
        };

        xhr.send(formData);
    }

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        formSubmitted = true;
        sendData();
    });

    form.addEventListener('input', function() {
        if (formSubmitted) {
            if (isFormValid()) {
                clearErrors();
            } else {
                sendData();
            }
        }
    });
});