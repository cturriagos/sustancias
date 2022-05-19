/**
 * Funcion que muestra ua ventana de informacion con un objeto que trae la informacion de estos.
 * @param {string|object|array} obj Contiene la informacion del mensaje de error que va a ser mostrado
 * @return {void} No retorna nada
 */
const message_error = (obj) => {
    let title = "¡Error!"
    try {
        if (typeof obj === "string") {
            let myObject = (0, eval)('(' + obj + ')');
            if (myObject) obj = myObject;
        }
    } catch (e) {
        //console.log(e);
    }
    let html = '';
    if (typeof (obj) === 'object') {
        title = "¡Errores!"
        html = '<ul style="text-align: left; padding-inline-start: unset;">';
        $.each(obj, function (key, value) {
            html += '<li style="display: block;">' + (key + 1) + ': ' + value + '</li>';
        });
        html += '</ul>';
    } else {
        html = '<p>' + obj + '</p>';
    }
    $.confirm({
        title: title,
        content: html,
        icon: 'fa fa-exclamation-triangle',
        theme: 'material',
        escapeKey: true,
        buttons: {
            ok: {
                text: "OK",
                keys: ['enter', 'esc'],
                btnClass: 'btn-primary',
                action: function () {

                }
            }
        }
    });
};

/**
 * Función que envia un mensaje de informacion al usuario a travez del plugin jqueryconfirm
 * @param {string} message Mensaje que va a ser mostrado al usuario
 * @param {function} callback Funcion de retorno que se activa cuando el usuario acepta el mensaje de información
 * @return {void} No retorna nada
 */
const message_info = (message, callback) => {
    $.confirm({
        title: '¡Notificación!',
        content: `<p>${message}</p>`,
        icon: 'fa fa-info',
        theme: 'material',
        autoClose: 'ok|5000',
        buttons: {
            ok: {
                text: "OK",
                keys: ['enter', 'esc'],
                btnClass: 'btn-primary',
                action: function () {
                    callback();
                }
            }
        }
    });
};


/**
 * Funcion que se encarga de buscar la cookie que ingresa como parametro y retorna su valor en caso
 * de encontrarla
 * @param {string} name Nombre de la cookie que va a ser buscada
 * @return {string} Retorna el valor de la cookie que fue buscada
 */
function getCookie(name) {
    let cookieValue = "";
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


/**
 * Funcion que recorre y muestra en consola la informacion de un formadata
 * @param {FormData} form_data Objeto formadata que sera recorrido
 * @return {void} No retorna nada
 */
const recorrer_formdata = form_data => {
    form_data.forEach(function (value, key, parent) {
        console.log(`${key}: ${value}`);
    });
};


/**
 * Esta funcion activa una ventana de confirmación preguntandole al usuario si desae o no enviar una información
 * al servidor a traves de una solicitud http
 * @param {string} url Dirección url a la cual va a ser enviada la información
 * @param {FormData} parameters Informacion que va aser enviada al servidor
 * @param {string} title Titulo de la ventana de confirmación
 * @param {string} content Contenido de la ventana de confirmacion
 * @param {function} callback Funcion que retorna la información del servidor cuando llega despues de la
 * solicitud http
 * @param {function} cancelOrError Funcion que se activa y retorna en caso de un error del servidor o
 * cancelar la accion
 * @return {void} No retorna nada
 */
const submit_with_ajax = (url, parameters, title, content, callback, cancelOrError) => {
    confirm_action(title, content,
        function () {
            $.blockUI();
            $.ajax({
                'url': url,
                'type': 'POST',
                'data': parameters,
                'dataType': 'json',
                'processData': false,
                'contentType': false
            }).done(function (data) {
                if (!data.hasOwnProperty('error')) {
                    callback(data);
                } else {
                    message_error(data.error);
                    cancelOrError(data.error)
                }
            }).fail(function (jqXHR, textStatus, errorThrown) {
                message_error(errorThrown);
                cancelOrError(errorThrown);
            }).always(function (data) {
                $.unblockUI();
            });
        }, function () {
            cancelOrError("");
        });
};


/**
 * Funcion que activa una ventana de confirmacion para realizar alguna opcion especifica
 * @param {string} title EL titulo de la ventana de confirmacion
 * @param {string} content EL contenido de la ventana de confirmación
 * @param {function} callback Funcion que se activa si el usuario confirma la accion
 * @param {function} cancel Funcion que retorna en caso de cancelar la accion
 * @return {void} No retorna nada
 */
const confirm_action = (title, content, callback, cancel) => {
    $.confirm({
        theme: 'material',
        title: title,
        icon: 'fa fa-info',
        content: content,
        columnClass: 'medium',
        typeAnimated: true,
        cancelButtonClass: 'btn-primary',
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: "Si",
                keys: ['enter'],
                btnClass: 'btn-primary',
                action: function () {
                    callback();
                }
            },
            danger: {
                text: "No",
                keys: ['esc'],
                btnClass: 'btn-red',
                action: function () {
                    cancel();
                }
            },
        }
    });
};


/**
 * Funcion que se encarga de trasformar un objeto en un string con formato de url
 * por ejemplo: {a: 1, b: 2} = ?a=1&b=2
 * @param {Object} params Corresponde a los parametros que va a formatear
 * @return {string} Retorna un string con la informacion formateada
 */
const encodeQueryString = (params = {}) => {
    const keys = Object.keys(params);
    return keys.length
        ? "?" + keys
        .map(key => encodeURIComponent(key)
            + "=" + encodeURIComponent(params[key]))
        .join("&")
        : "";
};


/**
 * Funcion que activa el plugin touchspin de jquery a uno o varios input que tienen cierto name especifico
 * @param {HTMLTableRowElement} row fila de un table en el que se va a buscar un input con un name especifico
 * para activarle el plugin touchspin
 * @param {string} nameInput Nombre(name) del input al que se le quere activar el plugin
 * @param {number} maxValue Parametro max del plugin TouchSpin de jquery
 * @param {number} minValue Parametro min del plugin TouchSpin de jquery
 * @param {number} initVal Parametro initval del plugin TouchSpin de jquery
 * @param {number} step Parametro step del plugin TouchSpin de jquery
 * @return {void} No retorna nada
 */
const activePluguinTouchSpinInputRow = (row, nameInput = "", maxValue = 0,
                                        minValue = 0, initVal = 0, step = 0) => {
    $(row).find(`input[name=${nameInput}]`).TouchSpin({
        'verticalbuttons': true,
        'min': minValue,
        'initval': initVal,
        'step': step,
        'max': maxValue,
        'forcestepdivisibility': 'none',
        'decimals': 4,
        'verticalupclass': 'glyphicon glyphicon-plus',
        'verticaldownclass': 'glyphicon glyphicon-minus',
        'buttondown_class': "btn btn-primary btn-sm",
        'buttonup_class': "btn btn-primary btn-sm"
    });
};

/**
 * Esta funcion activa un observador para el evento click que se realze dentro de una tabla en caso de ciertas
 * columnas se oculten cuando la tabla sea muy extensa(esto se puede ver en la documentacion de datatables jquery)
 * @param {string} tableId Corresponde al id de la tabla html que va a ser observada
 * @param {Object} dataTable corresponde al objeto del plugin datable de jquery a que se va a observar
 * @param {string} tagNameForEvent Corresponde al tag html que va a observar el evento
 * @param {function} updateRowsCallback se activa en caso de encontrar la fila dentro del datatable
 * al que se le activo un evento de click
 * @return {void} No retorna nada
 */
const addEventListenerOpenDetailRowDatatable = (tableId = "", dataTable,
                                                tagNameForEvent = "", updateRowsCallback) => {
    $(`#${tableId} tbody`).on('click', tagNameForEvent, function () {
        let tr = $(this).closest('tr');
        let row = dataTable.row(tr);
        let child = row.child();
        let data = row.data();
        if (child) {
            updateRowsCallback(child, data, row.index());
        }
    });
};


/**
 * Esta funcion realiza una peticion de informacion al servidor y la retorna a travez de callback
 * en caso de algun error en el serividor lo envia por error_call
 * @param {string} url La ulr a la cual se va a realizar la peticion
 * @param {Object} data Parametros que condicionales para obtener la informaion solicitada al servidor
 * @param {function} callback Funcion que se activa cuando la solicitud http recibe la informacion
 * solicitada (GET)
 * @param {function} error_call Funcion que se activa en caso de que la solicitud http retorne algun error
 * @return {void} No retorna nada
 */
const get_list_data_ajax = (url = "", data = {}, callback, error_call) => {
    url = `${url}${encodeQueryString(data)}`;
    fetch(url, {
        'method': 'GET',
        'credentials': 'include',
        'Content-Type': 'application/json',
        'headers': {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
        }
    }).then(function (response) {
        return response.json();
    }).then(function (json) {
        callback(json);
    }).catch(function (error) {
        error_call(error);
        console.error(error);
    });
};


/**
 * Esta funcion activa los eventos de los que usan los filtros de las datatables para filtrar informacion
 * y captura la informacion almacenada en ellos de acuerdo a la variable params que contiene los parametros
 * que requieren ser mapeados
 * @param {Object} params contiene un array de strings que representan la informacion que reuqere ser
 * mapeada de los filtros
 * @param {function} callback es una funcion de retorno que se activa despues de haber obtenido todos los
 * parametros
 * @return {void} No retorna nada
 */
const active_events_filters = (params, callback) => {
    $('ul[rel=lista_filtros]').find('a[rel=search]').on('click', function (evt) {
        let filter = this;
        $('ul[rel=lista_filtros]').find('a[rel=search]').parent().removeClass("active");
        $(filter.parentNode).addClass("active");
        let data_call = {}
        $.each(params, function (index, value) {
            data_call[index] = $(filter).data(index) || 0;
        });
        callback(data_call);
    });
};

/**
 * Esta funcion lee los parametros de la url y reemplaza los valores de los parametros iniciales
 * en caso de encontrarlos, y actualiza la url con el nuevo estado
 * @param {Object} initial Corresponde a los parametros iniciales
 * que retornaran en caso de no encontrarlos en la url
 * @return {Object} con los parametros mapeados de la url
 */
const get_url_params = (initial = {}) => {
    const urlParams = new URLSearchParams(window.location.search);
    const params = urlParams.entries();
    for (const entrie of params) {
        let property;
        let exist = false;
        for (property in initial) {
            if (entrie[0] === property) {
                exist = true;
                break;
            }
        }
        if (exist) {
            initial[property] = entrie[1];
        }
    }
    let _new_url = window.location.origin + window.location.pathname + encodeQueryString(initial);

    if (!equal(_new_url, window.location.href)) {
        history.pushState(null, null, _new_url);
    }

    actualizar_estado_filtros(initial);

    return initial;
};


/**
 * Funcion que activa el filtro deseado(tag A en el doc HTML) mapeando la informacion existente en ellos
 * @param {Object} data Los datos que se van a buscar el los filtros
 * @return {void} No retorna nada
 */
const actualizar_estado_filtros = (data) => {
    let filtros = $('ul[rel=lista_filtros]').find('a[rel=search]');
    filtros.parent().removeClass("active");
    $.each(filtros, function (index, value) {
        let equal = true;
        let _data_value = $(value).data();

        try {
            for (let property in _data_value) {
                // No verificamos datos de control de los filtros
                if (property !== "collapse") {
                    if (_data_value[property] != data[property]) {
                        equal = false;
                        break;
                    }
                }
            }
        } catch (e) {

        }

        if (equal) {
            $(value.parentNode).addClass("active");

            if (_data_value.hasOwnProperty("collapse")) {
                $(`#${_data_value['collapse']}`).collapse('show');
            }

            return false;
        }
    });
}