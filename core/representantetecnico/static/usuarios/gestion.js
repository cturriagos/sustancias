let data_loaded = false;
const usuarios = {
    'datatable': null,
    'data': {
        'usuarios': [],
        'roles': [
            {'id': 1, 'text': 'Representante tecnico', 'value': 'representante', 'select': false},
            {'id': 2, 'text': 'Técnico laboratorista', 'value': 'laboratorista', 'select': false},
            {'id': 3, 'text': 'Bodeguero', 'value': 'bodeguero', 'select': false},
        ],
        'estados': [
            {'id': 1, 'text': 'Habilitado', 'value': 'habilitado'},
            {'id': 2, 'text': 'Desabilitado', 'value': 'desabilitado'}
        ]
    },
    add_user_blank: function () {
        if (this.data.usuarios.length >= 3) {
            message_error("No puede crear usuarios por persona mas que el numero de roles de sistema");
            return false;
        }
        let new_user = {
            'id': -1,
            'username': '',
            'creat_dat': '',
            'ul_accs': '',
            'rol_selected': null,
            'estado_selected': null,
            'permit_delete': true
        };
        this.data.usuarios.push(new_user);
        this.list_users();
    },
    add_users: function (array = []) {
        $.each(array, function (idex, item) {

            if (item.is_act) item.estado_selected = usuarios.data.estados[0];
            else item.estado_selected = usuarios.data.estados[1];

            if (item.is_rep) item.rol_selected = usuarios.data.roles[0];
            if (item.is_lab) item.rol_selected = usuarios.data.roles[1];
            if (item.is_groc) item.rol_selected = usuarios.data.roles[2];

            item.permit_delete = false;
        });
        this.data.usuarios = array;
    },
    list_users: function () {
        if (this.datatable) {
            this.datatable.clear();
            this.datatable.rows.add(this.data.usuarios).draw();
        }
    },
    delete_user: function (index) {
        if (!this.data.usuarios[index].permit_delete) {
            message_error("Usuario registrado en el sistema, no se puede eliminar");
            return false;
        }
        this.data.usuarios.splice(index, 1);
        this.list_users();
    },
    get_users: function () {
        return this.data.usuarios;
    },
    set_estado_selected: function (indexData, idestado) {
        $.each(this.data.estados, function (index, item) {
            if (item.id === idestado) {
                usuarios.data.usuarios[indexData].estado_selected = item;
                return false;
            }
        });
    },
    set_rol_selected: function (indexData, idrol, row) {
        if (usuarios.data.usuarios[indexData].rol_selected &&
            usuarios.data.usuarios[indexData].rol_selected.id === idrol) {
            return false;
        }
        $.each(this.data.roles, function (index, item) {
            if (idrol === item.id) {
                usuarios.data.usuarios[indexData].rol_selected = item;
            }
        });
    },
    verify_rol_diferent: function () {
        let dif = true;
        $.each(this.data.roles, function (indexrol, rol) {
            rol.select = false;
        });
        $.each(this.data.roles, function (indexrol, rol) {
            $.each(usuarios.data.usuarios, function (indexuser, user) {
                if (rol.id === user.rol_selected.id) {
                    if (rol.select) {
                        dif = false
                        return false;
                    } else {
                        rol.select = true;
                    }
                }
            });
            if (!dif) {
                return false;
            }
        });
        return dif;
    },
    verify_send_data: function (callback, error) {
        if (!data_loaded) {
            message_info("Cargando...", function () {

            });
            return false;
        }
        if (!this.verify_rol_diferent()) {
            error("Debe seleccionar un rol diferente por cada usuario a agregar")
        } else {
            callback();
        }
    }
}

$(function () {
    usuarios.datatable = $('#tbroles').DataTable({
        'responsive': true,
        'autoWidth': true,
        'paging': false,
        'searching': false,
        'ordering': false,
        'info': false,
        'deferRender': true,
        'processing': true,
        'ajax': {
            'url': window.location.pathname,
            'type': 'GET',
            'data': function (d) {
                d.action = 'search_user_person';
            },
            "dataSrc": function (json) {
                data_loaded = true;
                usuarios.add_users(json);
                return usuarios.get_users();
            }
        },
        'columns': [
            {
                "className": 'show-data-hide-control',
                'data': 'id'
            },
            {'data': 'username'},
            {'data': 'id'},
            {'data': 'creat_dat'},
            {'data': 'ul_accs'},
            {'data': 'id'},
            {'data': 'id'}
        ],
        'columnDefs': [
            {
                'targets': [0],
                'render': function (data, type, row) {
                    return '<label style="font-weight: 500;" rel="num_user"></label>';
                }
            },
            {
                'targets': [2],
                'render': function (data, type, row) {
                    if (row.permit_delete) return '<select name="roles" class="form-control" style="width: 100%"></select>';
                    else return '<select name="roles" readonly="" disabled class="form-control" style="width: 100%"></select>';
                }
            },
            {
                'targets': [5],
                'render': function (data, type, row) {
                    return '<select name="estados" class="form-control" style="width: 100%"></select>';
                }
            },
            {
                'targets': [6],
                'render': function (data, type, row) {
                    if (row.permit_delete) return '<a rel="remove" class="btn btn-danger btn-flat"><i class="fas fa-trash"></i></a> ';
                    return ""
                }
            }
        ],
        'rowCallback': function (row, data, displayNum, displayIndex, dataIndex) {
            updateRowsCallback(row, data, dataIndex);
        }
    });

    //evento para agregar un nuevo usuario en blanco
    $('button[rel="add_user"]').on('click', function (event) {
        if (!data_loaded) {
            message_info("Cargando...", function () {

            });
            return false;
        }
        usuarios.add_user_blank();
    });

    // Add event listener for opening and closing details
    addEventListenerOpenDetailRowDatatable('tblistado', usuarios.datatable
        , 'td.show-data-hide-control',
        function (row, data, dataIndex) {
            updateRowsCallback(row, data, dataIndex);
        });


    function updateRowsCallback(row, data, dataIndex) {
        $(row).find('select[name="roles"]').on('change.select2', function (e) {
            let data_select = $(this).select2('data');
            usuarios.set_rol_selected(parseInt(dataIndex), parseInt(data_select[0].id), row);
        }).select2({
            'theme': 'bootstrap4',
            'language': 'es',
            'data': usuarios.data.roles,
            'containerCssClass': "select2-font-size-sm"
        });
        if (data.rol_selected) {
            $(row).find('select[name="roles"]').val(data.rol_selected.id);
        }
        $(row).find('select[name="roles"]').trigger('change.select2');

        $(row).find('label[rel="num_user"]').text(dataIndex + 1);

        $(row).find('select[name="estados"]').on('change.select2', function (e) {
            let data_select = $(this).select2('data');
            usuarios.set_estado_selected(parseInt(dataIndex), parseInt(data_select[0].id));
        }).select2({
            'theme': 'bootstrap4',
            'language': 'es',
            'data': usuarios.data.estados
        });

        if (data.estado_selected) {
            $(row).find('select[name="estados"]').val(data.estado_selected.id);
        }

        $(row).find('select[name="estados"]').trigger('change.select2');

        $(row).find('a[rel="remove"]').on('click', function (event) {
            confirm_action(
                'Alerta',
                `¿Esta seguro de eliminar el usuario ${data.email}? \n 
                Nota: Un usuario registrado en el sistema no sera eliminado, 
                pero su cuenta se desabilitara`,
                function () {
                    usuarios.delete_user(dataIndex);
                },
                function () {

                }
            );
        });
    }
});