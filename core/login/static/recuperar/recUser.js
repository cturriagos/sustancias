$(function () {
    //envio de datos al servidor
    $('#frmRecuperarUser').on('submit', function (event) {
        event.preventDefault();
        let form = this;
        let parameters = new FormData(form);
        let correo = parameters.get("correo");
        if (correo.length <= 0) {
            message_error("Ingrese el correo");
            return false;
        }
        submit_with_ajax(
            window.location.pathname
            , parameters
            , 'Confirmación'
            , '¿Estas seguro de realizar la siguiente acción?'
            , function (data) {
                message_info("Se ha enviado un mensaje a su correo",
                    function () {
                        location.href = "/"
                    });
            }, function () {
                $.unblockUI();
            }
        );
    });
});