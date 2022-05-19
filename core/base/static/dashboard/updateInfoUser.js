$(function () {
    const $seleccionArchivos = document.querySelector("#id_imagen_update"),
        $imagenPrevisualizacion = document.querySelector("#imagenUpdatePrevisualizacion");

    // Escuchar cuando cambie
    $seleccionArchivos.addEventListener("change", () => {
        // Los archivos seleccionados, pueden ser muchos o uno
        const archivos = $seleccionArchivos.files;
        // Si no hay archivos salimos de la función y quitamos la imagen
        if (!archivos || !archivos.length) {
            $imagenPrevisualizacion.src = "";
            return;
        }
        // Ahora tomamos el primer archivo, el cual vamos a previsualizar
        const primerArchivo = archivos[0];
        // Lo convertimos a un objeto de tipo objectURL
        // Y a la fuente de la imagen le ponemos el objectURL
        $imagenPrevisualizacion.src = URL.createObjectURL(primerArchivo);
    });

    //envio de datos al servidor
    $('#frmUpdateInfo').on('submit', function (event) {
        event.preventDefault();
        let form = this;
        let parameters = new FormData(form);
        submit_with_ajax(
            '/dashboard/', parameters
            , 'Confirmación'
            , '¿Estas seguro de realizar la siguiente acción?'
            , function (data) {
                location.reload();
            }, function () {
                $.unblockUI();
            }
        );
    });
});