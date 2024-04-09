document.getElementById('id_cover').addEventListener('change', function(e) {
    const file = e.target.files[0];
    const existingContainer = document.getElementById('cover-thumbnail-container');
    while (existingContainer.firstChild) {
        existingContainer.removeChild(existingContainer.firstChild);
    }
    if (!file || !file.type.startsWith('image/')) {
        alert('Выбранный файл не является изображением. Пожалуйста, выберите изображение.');
        e.target.value = '';
        return;
    }
    const reader = new FileReader();
    reader.onload = function(e) {
        const img = document.createElement('img');
        img.src = e.target.result;
        img.className = 'thumbnail';
        existingContainer.appendChild(img);
    };
    reader.readAsDataURL(file);
});