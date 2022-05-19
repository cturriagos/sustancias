function util() {
    // $('#tblistado tbody')
    //     .on('click', 'a[rel=viewstocksubstance]', function () {
    //         let trdata = tblistado.cell($(this).closest('td, li')).index();
    //         let row = $(`#tblistado tbody tr:eq(${trdata.row})`);
    //         let rowData = tblistado.row(row).data();
    //         tbstock.clear();
    //         tbstock.rows.add(rowData.stock).draw();
    //     });

    // $(row).find('input[name="cantidad"]').trigger("touchspin.updatesettings", {
    //     max: solicitud.data.sustancias[dataIndex].cantidad_bodega
    // });

    //datatable.rows({selected: false}).data();
    //datatable.row(row).select();
}

function get_list_data_ajax_loading(url = "", data = {}, callback) {
    $.blockUI()
    get_list_data_ajax(url, data,
        function (response) {
            $.unblockUI();
            callback(response);
        }, function (error) {
            $.unblockUI();
        });
}

function verObservacion(title = "", text = "", labelInput = "") {
    $("#modalObs").find('h5').text(title);
    $("#modalObs").find('label').text(labelInput);
    $("#modalObs").find('textarea').text(text);
    $("#modalObs").modal("show");
}

function update_cantiad_total_stock(stock = [], selector_input = "") {
    setTimeout(() => {
        let cantidad = 0;
        $.each(stock, function (index, item) {
            cantidad += parseFloat(item.cantidad);
        });
        $(selector_input).val(cantidad.toFixed(4));
    }, 1);
}

function activeSelectionRowDatatable(row, datatable) {
    datatable.$('tr.selected').removeClass('selected');
    $(row).addClass('selected');
}

function activePluginTOuchSpinInput(nameInput = "", min = 0, initval = 0) {
    $(`input[name=${nameInput}]`).TouchSpin({
        'verticalbuttons': true,
        'min': min,
        'initval': initval,
        'verticalupclass': 'glyphicon glyphicon-plus',
        'verticaldownclass': 'glyphicon glyphicon-minus'
    });
}

function autocompleteInput(nameInput = "", urlSend = "", data = {}, selectItemCallBack) {
    //activar el autocomplete en el buscador
    $(`input[name=${nameInput}`).focus().autocomplete({
        source: function (request, response) {
            data['term'] = request.term;
            const url = `${urlSend}${encodeQueryString(data)}`;
            fetch(url, {
                'method': 'GET',
                'credentials': 'include',
                'Content-Type': 'application/json',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
                },
            })
                .then(res => res.json())
                .then((json) => {
                    response(json);
                });
        },
        delay: 400,
        minLength: 1,
        select: function (event, ui) {
            event.preventDefault();
            selectItemCallBack(ui.item);
            $(this).val('');
        }
    });
}

async function send_petition_server(
    method = '', formdata = new FormData(),
    url = "", csrfmiddlewaretoken = "", callback, error) {

    $.blockUI()
    // Opciones por defecto estan marcadas con un *
    fetch(url, {
        method: method, // *GET, POST, PUT, DELETE, etc.
        mode: 'same-origin', // no-cors, *cors, same-origin
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
            'X-CSRFToken': csrfmiddlewaretoken
        },
        body: formdata // body data type must match "Content-Type" header
    }).then(function (response) {
        return response.json(); // parses JSON response into native JavaScript objects
    }).then(function (data) {
        if (data.hasOwnProperty("error")) error(data.error);
        else callback(data);
    }).catch(function (reason) {
        error(reason);
    }).finally(function () {
        $.unblockUI();
    });
}

function get_async_data_callback(url, data, callback, error) {
    Loading.show();
    $.ajax({
        'url': url,
        'type': 'POST',
        'data': data,
        'dataType': 'json'
    }).done(function (response) {
        if (!response.hasOwnProperty('error')) {
            if (response.length > 0) {
                Loading.hide();
                callback(response);
            }
            Loading.hide();
        } else {
            Loading.hide();
            error(response.error);
        }
    }).fail(function (jqXHR, textStatus, errorThrown) {
        Loading.hide();
        error(errorThrown);
    });
}

function update_datatable(datatable, url, data) {
    Loading.show();
    $.ajax({
        'url': url,
        'type': 'POST',
        'data': data,
        'dataType': 'json'
    }).done(function (response) {
        if (!response.hasOwnProperty('error')) {
            if (response.length > 0) {
                Loading.hide();
                datatable.clear();
                datatable.rows.add(response).draw();
            }
            Loading.hide();
        } else {
            Loading.hide();
            message_error(response.error);
        }
    }).fail(function (jqXHR, textStatus, errorThrown) {
        Loading.hide();
        message_error(errorThrown);
    });
}

function disableEnableForm(form, yesNo) {
    let f = form, s, opacity;
    s = f.style;
    opacity = yesNo ? '40' : '100';
    s.opacity = s.MozOpacity = s.KhtmlOpacity = opacity / 100;
    s.filter = 'alpha(opacity=' + opacity + ')';
    for (let i = 0; i < f.length; i++) f[i].disabled = yesNo;
}