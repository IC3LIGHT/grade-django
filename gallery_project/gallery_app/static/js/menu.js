function toggleMenu() {
    var menu = document.getElementById("menu");
    menu.style.display = menu.style.display === "none" ? "block" : "none";
}

document.addEventListener("click", function(event) {
    var menu = document.getElementById("menu");
    var button = document.querySelector(".button_menu");
    if (event.target !== menu && event.target !== button && menu.style.display === "block") {
        menu.style.display = "none";
    }
});