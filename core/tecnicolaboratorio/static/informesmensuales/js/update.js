let data_loaded = false;
const informe = {
    datatable: null,
    datatable_desgloses: null,
    data: {
        detalle_informe_selected: {'id': 0},
        detalleInforme: [],
        desglose_detalle: []
    },
    add_details: function (details) {
        $.each(details, function (index, item) {
            item.cantidad = parseFloat(item.cantidad);
            item.stock.cantidad_lab = parseFloat(item.stock.cantidad_lab);
            item.is_saved = true;
        });
        this.data.detalleInforme = details;
    },
    add_desglose_detalle: function (data) {
        let cantidad_total = 0;
        $.each(data, function (index, item) {
            item.cantidad = parseFloat(item.cantidad);
            cantidad_total += item.cantidad;
        });
        this.data.desglose_detalle = data;
        this.update_input_cantidad_desglose(cantidad_total);
    },
    add_sustancia: function (item) {
        item = this.config_item(item);
        if (this.verify_sustance_exist(item)) {
            message_error("Sustancia ya agregada");
            return false;
        }
        this.data.detalleInforme.push(item);
        this.list_sustancias();
    },
    clean_form_add_desglose: function () {
        $('#frmAgregarDesglose').find('input[name="documento"]').val("");
        $('#frmAgregarDesglose').find('input[name="cantidad"]').val(0);
        $('#frmAgregarDesglose').find('input[name="cantidad"]').trigger("touchspin.updatesettings", {
            max: 10000
        });
    },
    config_item: function (item) {
        return {
            'id': -1, 'cantidad': 0,
            'stock': {
                'id': item.id,
                'nombre': item.value,
                'cantidad_lab': parseFloat(item.cantidad_lab),
                'unidad_medida': item.unidad_medida
            },
            'is_saved': false,
        }
    },
    get_detalles: function () {
        return this.data.detalleInforme;
    },
    get_deglose_detalle: function () {
        return this.data.desglose_detalle;
    },
    list_sustancias: function () {
        this.datatable.clear();
        this.datatable.rows.add(this.data.detalleInforme).draw();
    },
    update_cantidad_sustancia: function (nueva_cantidad, index) {
        this.data.detalleInforme[index].cantidad = nueva_cantidad;
    },
    update_input_cantidad_desglose: function (value) {
        $('#frmDetalleConsumoSustanciaInforme').find('input[name=cantidad_desglose_total]').val(value);
    },
    verify_send_data: function (callback, error) {
        if (!data_loaded) {
            error("Cargando...");
            return false;
        }
        let isValidData = true;
        $.each(this.data.detalleInforme, function (index, item) {
            if (item.cantidad <= 0) {
                isValidData = false;
                error(`! La sustancia ${item.stock.nombre} tiene una cantidad a ingresar incorrecta, por favor verifique ¡`);
            }
        });
        if (isValidData) callback();
    },
    verify_sustance_exist: function (new_item) {
        let exist = false;
        $.each(this.data.detalleInforme, function (index, item) {
            if (new_item.stock.id === item.stock.id) {
                exist = true;
                return false;
            }
        });
        return exist;
    }
}
$(function () {
    let data_loaded_desglose = false;
    const csrfmiddlewaretoken = getCookie("csrftoken");

    informe.datatable = $('#tblistado').DataTable({
        'responsive': true,
        "ordering": false,
        "autoWidth": true,
        'info': false,
        'searching': false,
        'paging': false,
        "processing": true,
        "language": {
            "emptyTable": "",
            "zeroRecords": ""
        },
        'ajax': {
            'url': window.location.pathname,
            'type': 'GET',
            'data': function (d) {
                d.action = 'informe_detail';
            },
            "dataSrc": function (json) {
                data_loaded = true;
                informe.add_details(json);
                return informe.get_detalles();
            }
        },
        'columns': [
            {
                "className": 'show-data-hide-control',
                'data': 'id'
            },
            {'data': 'stock.nombre'},
            {'data': 'stock.unidad_medida'},
            {'data': 'stock.cantidad_lab'},
            {'data': 'cantidad'},
            {'data': 'id'}
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
                    return parseFloat(data).toFixed(4);
                }
            },
            {
                'targets': [4],
                'render': function (data, type, row) {
                    return '<input value="' + data + '" type="text" name="cantidad" class="form-control form-control-sm input-sm" autocomplete="off"/>';
                }
            },
            {
                'targets': [5],
                'render': function (data, type, row) {
                    if (row.id > 0 && row.is_saved) {
                        return '<a rel="movimientos" class="btn btn-info btn-flat"><i class="fas fa-people-carry"></i></a>';
                    } else {
                        return ""
                    }
                }
            }
        ],
        'rowCallback': function (row, data, displayNum, displayIndex, dataIndex) {
            updateRowsCallback(row, data, dataIndex);
        }
    });

    informe.datatable_desgloses = $('#tbdesglosesustanciainforme').DataTable({
        'responsive': true,
        "ordering": false,
        "autoWidth": true,
        'info': false,
        'searching': false,
        'paging': false,
        "processing": true,
        "language": {
            "emptyTable": "",
            "zeroRecords": "No existen desgloses registrados"
        },
        'ajax': {
            'url': '/informes-mensuales/desglose-sustancia/',
            'type': 'GET',
            'data': function (d) {
                d.action = 'search_desglose_sustancia';
                d.detalle_informe_id = informe.data.detalle_informe_selected.id;
            },
            "dataSrc": function (json) {
                data_loaded_desglose = true;
                informe.add_desglose_detalle(json);
                return informe.get_deglose_detalle();
            }
        },
        'columns': [
            {'data': 'proyecto'},
            {'data': 'cantidad'},
            {'data': 'documento'},
            {'data': 'id'},
        ],
        'columnDefs': [
            {
                'targets': [2],
                'orderable': false,
                'render': function (data, type, row) {
                    let html = '';
                    if (data && data.length > 0) {
                        html += '<a target="_blank" class="nav-link" style="text-align: center" href="' + data + '">Ver</a>';
                    } else {
                        html += 'No registrado';
                    }
                    return html;
                }
            },
            {
                'targets': [3],
                'render': function (data, type, row) {
                    return '<button rel="remove_desglose" type="button" class="btn btn-danger"><i class="fas fa-trash"></i></button>'
                }
            }
        ],
        'rowCallback': function (row, data, displayNum, displayIndex, dataIndex) {
            updateRowsCallbackDesgloses(row, data, dataIndex);
        }
    });

    //activar plugin select2 a los select del formulario
    $('.select2').select2({
        'theme': 'bootstrap4',
        'language': 'es'
    });

    $('input[name=search]').focus().autocomplete({
        source: function (request, response) {
            if (!data_loaded) {
                message_info("Cargando...", function () {

                });
                return false;
            }
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

    $('#frmAgregarDesglose').find('input[name=cantidad]').TouchSpin({
        'verticalbuttons': true,
        'min': 0,
        'initval': 0,
        'decimals': 4,
        'step': 0.1,
        'max': 10000,
        'forcestepdivisibility': 'none',
        'verticalupclass': 'glyphicon glyphicon-plus',
        'verticaldownclass': 'glyphicon glyphicon-minus'
    });

    $('#frmAgregarDesglose').find('input[name=csrfmiddlewaretoken]').val(csrfmiddlewaretoken);

    $('#modalDetalleConsumoSustanciaInforme').on('show.bs.modal', function (e) {
        informe.datatable_desgloses.ajax.reload();
    });

    function updateRowsCallback(row, data, dataIndex) {

        activePluguinTouchSpinInputRow(row, "cantidad", parseFloat(data.stock.cantidad_lab), 0, 0, 0.1);

        $(row).find('a[rel="remove"]').on('click', function (event) {
            confirm_action(
                'Notificación',
                '¿Esta seguro de eliminar la sustancia ¡' + data.stock.nombre + '!?',
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

        $(row).find('a[rel="movimientos"]').on('click', function (event) {
            informe.data.detalle_informe_selected = data;

            data_loaded_desglose = false;

            $('#frmDetalleConsumoSustanciaInforme').find('h5').text(`Lista de desgloses de sustancia ${data.stock.nombre}`)
            $('#frmDetalleConsumoSustanciaInforme').find('input[name="id_detalle"]').val(data.id);
            $('#frmDetalleConsumoSustanciaInforme').find('input[name="cantidad_consumida_registrada"]').val(data.cantidad);

            $('#modalDetalleConsumoSustanciaInforme').modal({
                backdrop: 'static',
                show: true
            });
        });
    }

    $('#frmDetalleConsumoSustanciaInforme').find('button[rel="btnSyncDesgl"]').on('click', function (event) {
        data_loaded_desglose = false;
        informe.datatable_desgloses.ajax.reload();
    });

    //evento para agregar un nuevo desglose de consumo de sustancia del informe
    $('#frmDetalleConsumoSustanciaInforme').find('button[rel="add_consumo"]').on('click', function (event) {
        if (!data_loaded_desglose) {
            message_info('Cargando...', function () {

            });
            return false;
        }

        let id_detalle = $('#frmDetalleConsumoSustanciaInforme').find('input[name="id_detalle"]').val();

        let cantidad_desglose_total = parseFloat($('#frmDetalleConsumoSustanciaInforme').find('input[name=cantidad_desglose_total]').val());
        let cantidad_consumo_mes = parseFloat($('#frmDetalleConsumoSustanciaInforme').find('input[name="cantidad_consumida_registrada"]').val());

        $('#frmAgregarDesglose').find('input[name="id_detalle"]').val(id_detalle);

        $('#frmAgregarDesglose').find('input[name="cantidad"]').trigger("touchspin.updatesettings", {
            max: cantidad_consumo_mes - cantidad_desglose_total
        });

        $('#modalDetalleConsumoSustanciaInforme').modal('toggle');

        $('#modalAgregarDesglose').modal({
            backdrop: 'static',
            show: true
        });
    });

    function updateRowsCallbackDesgloses(row, data, dataIndex) {
        $(row).find('button[rel="remove_desglose"]').on('click', function (event) {
            let parameters = new FormData();

            parameters.append("csrfmiddlewaretoken", csrfmiddlewaretoken);

            submit_with_ajax(
                `/informes-mensuales/desglose-sustancia/delete/${data.id}/`
                , parameters
                , 'Confirmación'
                , '¿Estas seguro de realizar la siguiente acción?'
                , function (data) {
                    informe.datatable_desgloses.ajax.reload();
                }, function (error) {
                    console.error(error);
                }
            );
        });
    }
});