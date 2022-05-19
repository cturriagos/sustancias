(function ($) {
    'use strict';

    // save the original plugin
    const _parent = $.fn.modal;

    // define your own constructor
    const Modal = function (element, options) {
        if (!arguments[0].hasOwnProperty('ismodal')) {
            arguments[0].ismodal = false;
        }

        if (arguments[0].ismodal) {
            return false;
        }

        _parent.Constructor.apply(this, arguments);

        arguments[0].ismodal = true
    };

    // set custom default options
    Modal.DEFAULTS = $.extend({}, _parent.Constructor.DEFAULTS, {
        backdrop: 'static',
        unclosable: false
    });

    // extend the prototype for your plugin from the original plugin
    Modal.prototype = $.extend({}, _parent.Constructor.prototype);

    // define a method for easy access to parent methods
    Modal.prototype.parent = function () {
        let args = $.makeArray(arguments),
            method = args.shift();
        _parent.Constructor.prototype[method].apply(this, args)
    };

    // override the show method to demonstrate
    Modal.prototype.show = function () {
        this.parent('show');
    };

    Modal.prototype.hide = function () {
        if (!this._config.unclosable) {
            this.parent('hide');
        }
    };

    // override the actual jQuery plugin method
    $.fn.modal = function (option, _relatedTarget) {

        return this.each(function () {
            let $this = $(this),
                data = $this.data('bs.modal'),
                options = $.extend({}, Modal.DEFAULTS, $this.data(), typeof option === 'object' && option);

            if (!data) {
                $this.data('bs.modal', (data = new Modal(this, options)));
            }

            if (typeof option === 'string') {
                data[option](_relatedTarget);
            } else if (options.show) {
                data.show(_relatedTarget);
            }
        });
    };

    // override the plugin constructor
    $.fn.modal.Constructor = Modal;

    // override the plugin no-conflict method
    $.fn.modal.noConflict = function () {
        $.fn.modal = _parent;
        return this;
    };

})(jQuery);