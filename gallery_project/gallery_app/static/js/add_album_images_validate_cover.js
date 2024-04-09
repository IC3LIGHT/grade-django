document.getElementById('id_cover').addEventListener('change', function(e) {
    const file = e.target.files[0];
    const existingContainer = document.getElementById('cover-thumbnail-container');
    if (existingContainer) {
        existingContainer.parentNode.removeChild(existingContainer);
    }

    if (!file || !file.type.startsWith('image/')) {
        alert('Выбранный файл не является изображением. Пожалуйста, выберите изображение.');
        e.target.value = '';
        return;
    }

    const coverContainer = document.createElement('div');
    coverContainer.id = 'cover-thumbnail-container';
    this.parentNode.insertBefore(coverContainer, this.nextSibling);

    const reader = new FileReader();
    reader.onload = function(e) {
        const img = document.createElement('img');
        img.src = e.target.result;
        img.className = 'thumbnail';
        coverContainer.appendChild(img);
    };
    reader.readAsDataURL(file);
});