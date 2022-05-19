const informe = {
    datatable: null,
    data: {
        sustancias: []
    },
    add_sustancia: function (item) {
        if (this.verify_sustance_exist(item)) {
            message_error("Sustancia ya agregada");
            return false;
        }
        item = this.config_item(item);
        this.data.sustancias.push(item);
        this.list_sustancias();
    },
    config_item: function (item) {
        item["cantidad_consumida"] = 0;
        return item
    },
    delete_sustancia: function (index) {
        this.data.sustancias.splice(index, 1);
        this.list_sustancias();
    },
    delete_all_sustancias: function () {
        if (this.data.sustancias.length === 0) return false;
        confirm_action(
            'Alerta',
            '¿Esta seguro de eliminar todas las sustancias del detalle?',
            function () {
                informe.data.sustancias = [];
                informe.list_sustancias();
            },
            function () {

            }
        );
    },
    list_sustancias: function () {
        this.datatable.clear();
        this.datatable.rows.add(this.data.sustancias).draw();
    },
    update_cantidad_sustancia: function (nueva_cantidad, index) {
        this.data.sustancias[index].cantidad_consumida = nueva_cantidad;
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
    verify_send_data: function (callback, error) {
        let isValidData = true;
        $.each(this.data.sustancias, function (index, item) {
            if (item.cantidad_consumida <= 0) {
                isValidData = false;
                error(`! La sustancia ${item.value} tiene una cantidad a ingresar invalida, por favor verifique ¡`);
            }
        });
        if (isValidData) callback();
    }
}

$(function () {

    informe.datatable = $('#tblistado').DataTable({
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
            {'data': 'cantidad_lab'},
            {'data': 'cantidad_consumida'}
        ],
        'columnDefs': [
            {
                'targets': [0],
                'orderable': false,
                'render': function (data, type, row) {
                    return '<a rel="remove" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash"></i></a> ';
                }
            },
            {
                'targets': [4],
                'orderable': false,
                'render': function (data, type, row) {
                    return '<input value="' + data + '" type="text" name="cantidad" class="form-control form-control-sm input-sm" autocomplete="off"/>';
                }
            }
        ],
        'rowCallback': function (row, data, displayNum, displayIndex, dataIndex) {
            updateRowsCallback(row, data, dataIndex);
        }
    });

    $('input[name=search]').focus().autocomplete({
        source: function (request, response) {
            let data = {
                'term': request.term,
                'action': "search_sus_lab"
            }
            get_list_data_ajax('/laboratorios/', data,
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
            informe.add_sustancia(ui.item);
            $(this).val('');
        }
    });

    // Add event listener for opening and closing details
    addEventListenerOpenDetailRowDatatable('tblistado', informe.datatable
        , 'td.show-data-hide-control',
        function (row, data, dataIndex) {
            updateRowsCallback(row, data, dataIndex);
        });

    //evento para limpiar el cuadro de busqueda de sustancias
    $('button[rel="cleansearch"]').on('click', function (event) {
        $('input[name="search"]').val("");
    });

    //evento para eliminar todas las sustancias del objeto manejador y el datatable
    $('button[rel="removeall"]').on('click', function (event) {
        informe.delete_all_sustancias();
    });

    let year_act = new Date().getFullYear();

    $('select[name=mes]').select2({
        'theme': 'bootstrap4',
        'language': 'es'
    });

    $('input[name=year]').on('change', function (evt) {
        get_list_data_ajax('/laboratorios/', {'action': 'search_months_dsp', 'year': $(this).val()}
            , function (response) {
                $('select[name=mes]').html('').select2({
                    'theme': 'bootstrap4',
                    'language': 'es',
                    'data': response
                });
            }, function (error) {
                console.log(error)
            });
    }).TouchSpin({
        'verticalbuttons': true,
        'min': year_act - 1,
        'max': year_act + 1,
        'step': 1,
        'verticalupclass': 'glyphicon glyphicon-plus',
        'verticaldownclass': 'glyphicon glyphicon-minus'
    });

    function updateRowsCallback(row, data, dataIndex) {

        activePluguinTouchSpinInputRow(row, "cantidad", parseFloat(data.cantidad_lab), 0, 0, 0.1);

        $(row).find('a[rel="remove"]').on('click', function (event) {
            confirm_action(
                'Notificación',
                '¿Esta seguro de eliminar la sustancia ¡' + data.value + '!?',
                function () {
                    informe.delete_sustancia(dataIndex);
                },
                function () {

                }
            );
        });

        $(row).find('input[name="cantidad"]').on('change', function (event) {
            let nueva_cantidad = parseFloat($(this).val());
            informe.update_cantidad_sustancia(nueva_cantidad, dataIndex);
        });
    }
});