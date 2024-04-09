window.onload = function() {
    var cards = document.querySelectorAll('.card');
    var maxHeight = 0;
    for (var i = 0; i < cards.length; i++) {
        if (cards[i].offsetHeight > maxHeight) {
            maxHeight = cards[i].offsetHeight;
        }
    }
    for (var i = 0; i < cards.length; i++) {
        cards[i].style.height = maxHeight + 'px';
    }
};