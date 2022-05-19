$.contextMenu.handle.layerClick = function (e) {
    var $this = $(this),
        root = $this.data('contextMenuRoot'),
        button = e.button,
        x = e.pageX,
        y = e.pageY,
        fakeClick = x === undefined,
        target,
        offset,
        $win = $(window);

    setTimeout(function () {
        // If the click is not real, things break: https://github.com/swisnl/jQuery-contextMenu/issues/132
        if (fakeClick) {
            if (root !== null && typeof root !== 'undefined' && root.$menu !== null && typeof root.$menu !== 'undefined') {
                root.$menu.trigger('contextmenu:hide');
            }
            return;
        }

        var $window;
        var triggerAction = ((root.trigger === 'left' && button === 0) || (root.trigger === 'right' && button === 2));

        // find the element that would've been clicked, wasn't the layer in the way
        if (document.elementFromPoint && root.$layer) {
            root.$layer.hide();
            target = document.elementFromPoint(x - $win.scrollLeft(), y - $win.scrollTop());
            // also need to try and focus this element if we're in a contenteditable area,
            // as the layer will prevent the browser mouse action we want
            if (target.isContentEditable) {
                var range = document.createRange(),
                    sel = window.getSelection();
                range.selectNode(target);
                range.collapse(true);
                sel.removeAllRanges();
                sel.addRange(range);
            }
            $(target).trigger(e);
            root.$layer.show();
        }

        if (root.hideOnSecondTrigger && triggerAction && root.$menu !== null && typeof root.$menu !== 'undefined') {
            root.$menu.trigger('contextmenu:hide');
            return;
        }

        if (root.reposition && triggerAction) {
            if (document.elementFromPoint) {
                if (root.$trigger.is(target)) {
                    root.position.call(root.$trigger, root, x, y);
                    return;
                }
            } else {
                offset = root.$trigger.offset();
                $window = $(window);
                // while this looks kinda awful, it's the best way to avoid
                // unnecessarily calculating any positions
                offset.top += $window.scrollTop();
                if (offset.top <= e.pageY) {
                    offset.left += $window.scrollLeft();
                    if (offset.left <= e.pageX) {
                        offset.bottom = offset.top + root.$trigger.outerHeight();
                        if (offset.bottom >= e.pageY) {
                            offset.right = offset.left + root.$trigger.outerWidth();
                            if (offset.right >= e.pageX) {
                                // reposition
                                root.position.call(root.$trigger, root, x, y);
                                return;
                            }
                        }
                    }
                }
            }
        }

        if (target && triggerAction) {
            root.$trigger.one('contextmenu:hidden', function () {
                $(target).contextMenu({x: x, y: y, button: button});
            });
        }

        if (!triggerAction) {
            $(target).trigger("click");
        }

        if (root !== null && typeof root !== 'undefined' && root.$menu !== null && typeof root.$menu !== 'undefined') {
            root.$menu.trigger('contextmenu:hide');
        }
    }, 50);
};