document.addEventListener("DOMContentLoaded", function() {
    const abrirBtn = document.querySelector(".abrir-menu");
    const cerrarBtn = document.querySelector(".cerrar-menu");
    const nav = document.querySelector(".nav");
    const overlay = document.querySelector(".overlay");
    const dropdownCuenta = document.getElementById("dropdownCuenta");
    const dropdownMenu = dropdownCuenta.querySelector(".dropdown-menu");

    // Abre el menú al hacer clic en el botón abrir
    abrirBtn.addEventListener("click", function(event) {
        event.stopPropagation();
        nav.classList.add("visible");
        overlay.classList.add("visible"); // Muestra el overlay
    });

    // Cierra el menú al hacer clic en el botón cerrar
    cerrarBtn.addEventListener("click", function(event) {
        event.stopPropagation();
        nav.classList.remove("visible");
        overlay.classList.remove("visible"); // Oculta el overlay
    });

    // Cierra el menú al hacer clic fuera del área del menú o en el overlay
    overlay.addEventListener("click", function() {
        if (nav.classList.contains("visible")) {
            nav.classList.remove("visible");
            overlay.classList.remove("visible"); // Oculta el overlay
        }
    });

    document.addEventListener("click", function(event) {
        if (nav.classList.contains("visible") && !nav.contains(event.target) && !abrirBtn.contains(event.target)) {
            nav.classList.remove("visible");
            overlay.classList.remove("visible"); // Oculta el overlay
        }
    });
        
    
        // Abre el menú al pasar el mouse por encima del botón
    dropdownCuenta.addEventListener("mouseenter", function() {
        dropdownMenu.classList.add("show");
    });

    // Cierra el menú al retirar el mouse del área del dropdown
    dropdownCuenta.addEventListener("mouseleave", function() {
        dropdownMenu.classList.remove("show");
    });

    
    
});
