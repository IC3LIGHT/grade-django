document.getElementById('albumPhotos').addEventListener('change', function(e) {
    const files = e.target.files;
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
});