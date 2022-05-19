const CSCSF = {
    "data": null,
    "data_initial": null,
    "initial": false,
    "datatable": null,
    "autoWidthDatatable": true,
    "init": function (params) {
        this.data_initial = params;
        this.data = JSON.parse(JSON.stringify(this.data_initial));
        get_url_params(this.data);
    },
    "init_events_datatable": function () {
        active_events_filters(CSCSF.data, function (data_send) {
            if (!equal(CSCSF.data_initial, data_send, {'nonStrict': true})) {
                CSCSF.data = data_send;
                history.pushState(null, null, window.location.origin + window.location.pathname + encodeQueryString(CSCSF.data));
            }
        });

        $('button[rel="btnSync"]').on('click', function (event) {
            if (!equal(CSCSF.data, CSCSF.data_initial, {'nonStrict': true})) {
                CSCSF.data = JSON.parse(JSON.stringify(CSCSF.data_initial));
                history.pushState(null, null, window.location.origin + window.location.pathname + encodeQueryString(CSCSF.data));
            }
        });

        window.addEventListener('locationchange', function (evt) {
            if (CSCSF.initial && CSCSF.datatable) {
                CSCSF.datatable.ajax.reload();
            }
        });
    },
    "activeCustomAutoWidth": function (idObserve) {
        if (!this.autoWidthDatatable) {
            const resizeObserverRepositorio = new ResizeObserver(entries => {
                if (CSCSF.datatable) {
                    setTimeout(function () {
                        CSCSF.datatable.columns.adjust();
                    }, 100)
                }
            });
            resizeObserverRepositorio.observe(document.getElementById(idObserve));
        }
    }
};