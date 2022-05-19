const repositorio = {
    datatable: null,
    urlrepository: null,
    cookie: getCookie("csrftoken"),
    data: {'action': 'searchcontent', 'type': 'repository', 'code': 0, 'url': window.location.pathname},
    actualizar_ruta: function (rutas) {
        let parent = $('#rutasrepositorio');
        let name = $('ul[rel=lista_filtros]').find(`a[data-type=${this.data.type}]`).find('span').text();
        let home = $(`<li class="breadcrumb-item"><a style="cursor:pointer;" rel="link-ruta" data-id="0">${name}</a></li>`);

        parent.html("").append(home);

        for (let i = rutas.length; i > 0; i--) {
            let item = rutas[i - 1];
            let ruta = $(`<li class="breadcrumb-item"><a style="cursor:pointer;" rel="link-ruta" data-id="${item.id}">${item.nombre}</a></li>`);

            parent.append(ruta);
        }

        this.activar_events_actualizar_ruta();
    },
    activar_events_actualizar_ruta: function f() {
        $('#rutasrepositorio').find('a[rel=link-ruta]').on('click', function (evt) {
            let filter = this;

            $('#rutas-repositorio').find('a[rel=link-ruta]').removeClass("active");

            $(filter).addClass("active");

            let id = parseInt($(filter).data('id'));

            if (id > 0) {
                let parent = {'id': id, 'is_dir': true};

                history.pushState(parent, null, window.location.origin + repositorio.urlrepository + parent.id + '/');
            } else {
                history.pushState(null, null, window.location.origin + repositorio.urlrepository);
            }
        });
    },
    change_menu_general: function () {
        $.contextMenu('destroy', '#context-menu-file');
        switch (this.data.type) {
            case "repository":
                this.create_general_menu_mi_rep();
                break;
            case "archgen":
            case "archext":
                this.create_general_menu_arch_ext();
                break;
            case "recicle":
                this.create_general_menu_papelera();
                break;
        }
    },
    create_general_menu_mi_rep: function () {
        $.contextMenu({
            selector: '#context-menu-file',
            callback: function (key, options) {

            },
            items: {
                "newfolder": {
                    name: "Nueva carpeta",
                    icon: "fas fa-folder-plus",
                    callback: function (itemKey, opt, e) {
                        //modalNewFolder
                        $('#modalNewFolder').modal('show');
                        // close the menu after clicking an item
                        return true;
                    }
                },
                "upload": {
                    name: "Subir archivo",
                    icon: "fas fa-upload",
                    callback: function (itemKey, opt, e) {
                        $("#myFile").click();
                        return true;
                    }
                },
                "sep1": "---------",
                "quit": {
                    name: "Quit",
                    icon: function () {
                        return 'context-menu-icon context-menu-icon-quit';
                    }
                }
            }
        });
    },
    create_general_menu_arch_ext: function () {
        $.contextMenu({
            selector: '#context-menu-file',
            callback: function (key, options) {

            },
            items: {
                "upload": {
                    name: "Subir archivo",
                    icon: "fas fa-upload",
                    callback: function (itemKey, opt, e) {
                        $('#modalNewFile').modal('show');
                        return true;
                    }
                },
                "sep1": "---------",
                "quit": {
                    name: "Quit",
                    icon: function () {
                        return 'context-menu-icon context-menu-icon-quit';
                    }
                }
            }
        });
    },
    create_general_menu_papelera: function () {
        $.contextMenu({
            selector: '#context-menu-file',
            callback: function (key, options) {

            },
            items: {
                "quit": {
                    name: "Quit",
                    icon: function () {
                        return 'context-menu-icon context-menu-icon-quit';
                    }
                }
            }
        });
    },
    actions_item: function (data, action) {
        let parameters = new FormData();

        parameters.append("csrfmiddlewaretoken", this.cookie);
        parameters.append("action", action);
        parameters.append("id", data.id);

        $.blockUI();
        $.ajax({
            'url': window.location.pathname,
            'type': 'POST',
            'data': parameters,
            'dataType': 'json',
            'processData': false,
            'contentType': false
        }).done(function (data) {
            if (!data.hasOwnProperty('error')) {
                repositorio.datatable.ajax.reload();
            } else {
                message_error(data.error);
            }
            $.unblockUI();
        }).fail(function (jqXHR, textStatus, errorThrown) {
            message_error(errorThrown);
            $.unblockUI();
        }).always(function (data) {
            $.unblockUI();
        });
    },
    delete_item: function (data) {
        this.actions_item(data, "deleteitem");
    },
    restaurar_item: function (data) {
        this.actions_item(data, "restoreitem");
    },
    descargar_archivo: function (url, nombre) {
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        // the filename you want
        a.download = nombre;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    },
    disable_enable_contextmenu: function (enabled = true, selector = '') {
        const $trigger = $(`${selector}`);
        if ($trigger.hasClass('context-menu-disabled')) {
            $trigger.contextMenu(enabled);
        } else {
            $trigger.contextMenu(enabled);
        }
    },
    recalculate_height: function (evt) {
        let height = 0;
        let _repo = $("#context-menu-file");
        let _parent = _repo.parent();
        height += _parent[0].clientHeight;
        $.each(_parent.children(), function (index, value) {
            let _value = $(value);
            if (_repo.prop("id") !== _value.prop("id")) {
                height -= value.clientHeight;
            }
        });
        _repo.css("minHeight", height - 1);
    }
}
$(function () {
    repositorio.change_menu_general();
    repositorio.datatable = $('#tblistado').DataTable({
        'deferRender': true,
        'processing': true,
        "scrollX": true,
        //'scrollY': '55vh',
        //'scrollCollapse': true,
        'ordering': false,
        'paging': false,
        'searching': false,
        'info': false,
        "language": {
            "emptyTable": "",
            "zeroRecords": ""
        },
        'ajax': {
            'url': window.location.pathname,
            'type': 'GET',
            'data': function (d) {
                d.action = repositorio.data.action;
                d.type = repositorio.data.type;
                d.code = repositorio.data.code;
            },
            "dataSrc": function (json) {
                repositorio.urlrepository = json.urlrepository;
                repositorio.actualizar_ruta(json.ruta);
                return json.data;
            }
        },
        'columns': [
            {'data': 'id'},
            {'data': 'nombre'},
            {'data': 'create_date'},
        ],
        'columnDefs': [
            {
                'targets': [1],
                'render': function (data, type, row) {
                    if (row.is_dir) {
                        return `<div style="display: flex"><i class="fas fa-folder fa-2x"></i>&nbsp <span>${data}</span></div>`;
                    } else if (row.is_file) {
                        return `<div style="display: flex"><i class="far fa-file-pdf fa-2x"></i>&nbsp <span>${data}</span></div>`;
                    }
                    return data;
                }
            }
        ],
        'rowCallback': function (row, data, displayNum, displayIndex, dataIndex) {
            updateRowsCallback(row, data, dataIndex)
        }
    });

    function updateRowsCallback(row, data, dataIndex) {
        if (data.is_recicler) {
            $(row).addClass('item-recicler');
        } else {
            $(row).on('dblclick', function (event) {
                history.pushState(data, null, window.location.origin + repositorio.urlrepository + data.id + '/');
            });
            if (data.is_dir) $(row).addClass('item-repository-folder');
            else if (data.is_file) $(row).addClass('item-repository-file');
        }
        $(row).css("cursor", "pointer");
    }

    active_events_filters(repositorio.data, function (data_send) {
        repositorio.data = data_send;
        repositorio.change_menu_general();

        if (window.location.pathname !== data_send['url']) {
            history.pushState(null, null, window.location.origin + data_send['url']);
            return false;
        }

        repositorio.datatable.ajax.reload();
    });

    $('#tblistado tbody').on('click contextmenu', 'tr', function () {
        if (!$(this).hasClass('selected')) {
            repositorio.datatable.$('tr.selected').removeClass('selected');

            $(this).addClass('selected');
        }
        //$(this).removeClass('selected');
    });
});

window.addEventListener('locationchange', function (evt) {
    let data = evt.detail;
    if (data) {
        if (data.is_dir) {
            repositorio.data.code = data.id;
            repositorio.datatable.ajax.url(window.location.pathname).load();
            return false;
        }
        if (data.is_file) {
            viewFile(data);
            return false;
        }
    }
    repositorio.datatable.ajax.url(window.location.pathname).load();
});
/**
 const resizeObserverRepositorio = new ResizeObserver(entries => {
    if (repositorio.datatable) {
        setTimeout(function () {
            repositorio.datatable.columns.adjust();
        }, 100)
    }
});

 resizeObserverRepositorio.observe(document.getElementById("context-menu-file"));
 */

// recalculate on resize
window.addEventListener('resize', repositorio.recalculate_height, false);
// recalculate on dom load
document.addEventListener('DOMContentLoaded', repositorio.recalculate_height, false);
// recalculate on load (assets loaded as well)
window.addEventListener('load', repositorio.recalculate_height);