var expr = /^[a-zA-Z0-9_\.\-]+@[a-zA-Z0-9\-]+\.[a-zA-Z0-9\-\.]+$/;

$(document).ready(function(){
    $("#bEnviar").click(function(event){
        event.preventDefault();
        
        var nombre = $("#itNombre").val();
        var apellido = $("#itApellido").val();
        var correo = $("#itCorreo").val();
        var telefono = $("#itTelefono").val();
        var mensaje = $("#itMensaje").val();
        var valid = true;

        // Validaciones
        if (nombre === "" || nombre === null) {
            $("#mensaje1").fadeIn();
            valid = false;
        } else {
            $("#mensaje1").fadeOut();
        }

        if (apellido === "" || apellido === null) {
            $("#mensaje2").fadeIn();
            valid = false;
        } else {
            $("#mensaje2").fadeOut();
        }

        if (correo === "" || correo === null || !expr.test(correo)) {
            $("#mensaje3").fadeIn();
            valid = false;
        } else {
            $("#mensaje3").fadeOut();
        }

        if (telefono === "" || telefono === null || telefono.length !== 9) {
            $("#mensaje4").fadeIn();
            valid = false;
        } else {
            $("#mensaje4").fadeOut();
        }

        if (mensaje === "" || mensaje === null || (mensaje.length > 500 || mensaje.length < 1)) {
            $("#mensaje5").fadeIn();
            valid = false;
        } else {
            $("#mensaje5").fadeOut();
        }

        if (valid) {
            alert("Formulario enviado con exito");
            $('#miFormulario').submit();
        }
    });
});