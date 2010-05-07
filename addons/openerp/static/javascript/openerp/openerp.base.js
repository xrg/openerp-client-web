// link probably expects faster feedback than form
var LINK_WAIT_NO_SIGN = 300;
var FORM_WAIT_NO_SIGN = 500;
jQuery(document).ready(function () {
    var app = jQuery('#appContent');
    if (app.length) {
        var waitBox = new openerp.ui.WaitBox();
        // open un-targeted links in #appContent via xhr. Links with @target are considered
        // external links
        jQuery(document).delegate('a[href]:not([target])', 'click', function (e) {
            var waitBoxTimeout = setTimeout(function () {
                delete waitBoxTimeout;
                waitBox.show();
            }, LINK_WAIT_NO_SIGN);
            app.load(jQuery(this).attr('href'), function () {
                if(typeof(waitBoxTimeout) != 'undefined') {
                    clearTimeout(waitBoxTimeout);
                    delete waitBoxTimeout;
                }
                waitBox.hide();
            });
            return false;
        });
        // do the same for forms
        jQuery(document).delegate('form:not([target])', 'submit', function (e) {
            var form = jQuery(this);
            // Don't make the wait box appear immediately
            var waitBoxTimeout = setTimeout(function () {
                delete waitBoxTimeout;
                waitBox.show();
            }, FORM_WAIT_NO_SIGN);
            jQuery.ajax({
                url: form.attr("action"),
                data: form.serialize(),
                method: form.attr('method') || 'GET',
                contentType: form.attr('enctype') || 'application/x-www-form-urlencoded',
                success: jQuery.proxy(app, 'html'),
                complete: function () {
                    // cancel wait box if we returned before timer triggered
                    if(typeof(waitBoxTimeout) != 'undefined') {
                        clearTimeout(waitBoxTimeout);
                        delete waitBoxTimeout;
                    }
                    waitBox.hide();
                }
            });
            return false;
        });
    }
});
