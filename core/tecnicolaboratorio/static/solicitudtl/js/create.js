const solicitud = {
    datatable: null,
    data: {
        sustancias: [],
        bodega_selected: null
    },
    add_sustancia: function (item) {
        if (this.verify_sustance_exist(item)) {
            message_error("Sustancia ya agregada");
            return false;
        }
        if (this.verify_bod_diferent()) {
            message_error("Solo puede agregar sustancias al informe de una sola bodega seleccionado");
            return false;
        }
        this.config_item(item);
        if (item.cantidad_bodega <= 0) {
            message_error("La sustancia seleccionada no tiene stock suficente en bodega");
            return false;
        }
        this.data.sustancias.push(item);
        this.list_sustancia();
    },
    config_item: function (item) {
        item.cantidad_solicitud = 0;
        item.cupo_autorizado = parseFloat(item.cupo_autorizado);
        item.cantidad_bodega = parseFloat(item.cantidad_bodega);
        item.bodega_selected = {'id': parseInt(this.data.bodega_selected.id), 'text': this.data.bodega_selected.text}
        return item;
    },
    list_sustancia: function () {
        this.datatable.clear();
        this.datatable.rows.add(this.data.sustancias).draw();
    },
    update_bodega_seleted: function (bod_item) {
        if (bod_item) this.data.bodega_selected = bod_item;
    },
    update_cantidad_sustancia: function (nueva_cantidad, index) {
        this.data.sustancias[index].cantidad_solicitud = nueva_cantidad;
    },
    delete_sustancia: function (index) {
        this.data.sustancias.splice(index, 1);
        this.list_sustancia();
    },
    delete_all_sustancias: function () {
        if (this.data.sustancias.length === 0) return false;
        confirm_action(
            'Alerta',
            '¿Esta seguro de eliminar todas las sustancias del detalle?',
            function () {
                solicitud.data.sustancias = [];
                solicitud.list_sustancia();
            },
            function () {

            }
        );
    },
    verify_bod_diferent: function () {
        let diferent = false;
        $.each(this.data.sustancias, function (index, item) {
            if (item.bodega_selected.id !== parseInt(solicitud.data.bodega_selected.id)) {
                diferent = true;
                return false;
            }
        });
        return diferent;
    },
    verify_send_data: function (callback, error) {
        let isValidData = true;
        if (this.data.sustancias.length === 0) {
            isValidData = false;
            error("¡Debe existir al menos 1 sustancia agregada en la solicitud!");
        } else {
            $.each(this.data.sustancias, function (index, item) {
                if (item.cantidad_solicitud <= 0) {
                    isValidData = false;
                    error(`! La sustancia ${item.value} tiene una cantidad a solicitar invalida, por favor verifique ¡`);
                }
            });
        }
        if (isValidData) callback();
    },
    verify_sustance_exist: function (new_item) {
        let exist = false;
        $.each(this.data.sustancias, function (index, item) {
            if (new_item.id === item.id) {
                exist = true;
                return false;
            }
        });
        return exist;
    },
}

$(function () {

    solicitud.datatable = $('#tblistado').DataTable({
        'responsive': true,
        "ordering": false,
        "autoWidth": true,
        'info': false,
        'searching': false,
        'paging': false,
        "language": {
            "emptyTable": "",
            "zeroRecords": ""
        },
        'columns': [
            {
                "className": 'show-data-hide-control',
                'data': 'id'
            },
            {'data': 'value'},
            {'data': 'unidad_medida'},
            {'data': 'cantidad_solicitud'},
            {'data': 'bodega_selected.text'},
            {'data': 'cantidad_bodega'}
        ],
        'columnDefs': [
            {
                'targets': [0],
                'render': function (data, type, row) {
                    return '<a rel="remove" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash"></i></a> ';
                }
            },
            {
                'targets': [3],
                'render': function (data, type, row) {
                    return '<input value="' + data + '" type="text" name="cantidad" class="form-control form-control-sm input-sm" autocomplete="off"/>';
                }
            },
            {
                'targets': [5],
                'render': function (data, type, row) {
                    return `<label style="font-weight: 500;" rel="cantidad_bodega">${parseFloat(data).toFixed(4)}</label>`;
                }
            }
        ],
        'rowCallback': function (row, data, displayNum, displayIndex, dataIndex) {
            updateRowsCallback(row, data, dataIndex);
        }
    });

    //activar plugin select2 a los select del formulario
    $('.select2').select2({
        'theme': 'bootstrap4',
        'language': 'es'
    });

    $('select[name=bodega]').on('change.select2', function (e) {
        let data_select = $(this).select2('data');
        solicitud.update_bodega_seleted(data_select[0]);
    }).select2({
        'theme': 'bootstrap4',
        'language': 'es'
    });
    $('select[name=bodega]').trigger('change.select2');

    $('input[name=search]').focus().autocomplete({
        source: function (request, response) {
            let code_bod = solicitud.data.bodega_selected
                ? solicitud.data.bodega_selected.id.length > 0
                    ? parseInt(solicitud.data.bodega_selected.id)
                    : 0
                : 0;
            if (code_bod === 0) {
                message_info("Bodega no seleccionada", function () {

                });
                return false;
            }
            let data = {
                'term': request.term,
                'action': "search_sus_bod_lab",
                'code_bod': code_bod
            }
            get_list_data_ajax('/sustancias/', data,
                function (res_data) {
                    response(res_data);
                }, function (error) {
                    message_error(error);
                });
        },
        delay: 400,
        minLength: 1,
        select: function (event, ui) {
            event.preventDefault();
            solicitud.add_sustancia(ui.item);
            $(this).val('');
        }
    });

    // Add event listener for opening and closing details
    addEventListenerOpenDetailRowDatatable('tblistado', solicitud.datatable
        , 'td.show-data-hide-control'
        , function (row, data, dataIndex) {
            updateRowsCallback(row, data, dataIndex);
        });

    //evento para limpiar el cuadro de busqueda de sustancias
    $('button[rel="cleansearch"]').on('click', function (event) {
        $('input[name="search"]').val("");
    });

    //evento para eliminar todas las sustancias del objeto manejador y el datatable
    $('button[rel="removeall"]').on('click', function (event) {
        solicitud.delete_all_sustancias();
    });

    function updateRowsCallback(row, data, dataIndex) {

        activePluguinTouchSpinInputRow(row, "cantidad", data.cupo_autorizado,
            0, 0, 0.1);

        $(row).find('input[name="cantidad"]').on('change', function (event) {
            let nueva_cantidad = parseFloat($(this).val());
            solicitud.update_cantidad_sustancia(nueva_cantidad, dataIndex);
        });
        $(row).find('a[rel="remove"]').on('click', function (event) {
            confirm_action(
                'Notificación',
                '¿Esta seguro de eliminar la sustancia ¡' + data.value + '!?',
                function () {
                    solicitud.delete_sustancia(dataIndex);
                },
                function () {

                }
            );
        });
    }
});