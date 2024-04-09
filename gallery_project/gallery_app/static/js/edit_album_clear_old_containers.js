    document.getElementById('albumPhotos').addEventListener('change', function(e) {
    const files = e.target.files;
    const thumbnailsContainer = document.getElementById('thumbnails-container');
    const existingThumbnailsContainer = document.getElementById('existing-thumbnails-container');
    if (files.length > 0) {
        while (existingThumbnailsContainer.firstChild) {
            existingThumbnailsContainer.removeChild(existingThumbnailsContainer.firstChild);
        }
        thumbnailsContainer.innerHTML = '';
    }

    let isValid = true;
    Array.from(files).forEach(file => {
        if (!file.type.startsWith('image/')) {
            alert('Один или несколько выбранных файлов не являются изображениями. Пожалуйста, выберите только изображения.');
            isValid = false;
        }
    });

    if (!isValid) {
        e.target.value = '';
        return;
    }

    Array.from(files).forEach((file, index) => {
        const reader = new FileReader();
        reader.onload = function(e) {
            const wrapper = document.createElement('div');
            wrapper.classList.add('thumbnail-wrapper');

            const img = document.createElement('img');
            img.src = e.target.result;
            img.classList.add('thumbnail');

            const input = document.createElement('input');
            input.type = 'text';
            input.classList.add('form-control');
            input.placeholder = 'Описание...';
            input.name = `description_new_${index}`;

            wrapper.appendChild(img);
            wrapper.appendChild(input);
            thumbnailsContainer.appendChild(wrapper);
        };
        reader.readAsDataURL(file);
    });
});