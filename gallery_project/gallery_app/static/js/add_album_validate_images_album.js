document.getElementById('albumPhotos').addEventListener('change', function(e) {
    const files = e.target.files;
    let isValid = true;

    Array.from(files).forEach(file => {
        if (!file.type.startsWith('image/')) {
            alert(`Один или несколько выбранных файлов не являются изображениями. Пожалуйста, выберите только изображения.`);
            isValid = false;
        }
    });

    if (!isValid) {
        e.target.value = '';
        document.getElementById('thumbnails-container').innerHTML = '';
        return;
    }

    const container = document.getElementById('thumbnails-container');
    container.innerHTML = '';

    Array.from(files).forEach((file, index) => {
        const reader = new FileReader();
        reader.onload = function(e) {
            const wrapper = document.createElement('div');
            wrapper.className = 'thumbnail-wrapper';

            const img = document.createElement('img');
            img.src = e.target.result;
            img.className = 'thumbnail';

            const input = document.createElement('input');
            input.type = 'text';
            input.placeholder = 'Описание...';
            input.name = `description_${index}`;

            wrapper.appendChild(img);
            wrapper.appendChild(input);
            container.appendChild(wrapper);
        };
        reader.readAsDataURL(file);
    });
});