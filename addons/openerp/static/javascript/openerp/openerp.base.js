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
            waitBox.showAfter(LINK_WAIT_NO_SIGN);
            app.load(jQuery(this).attr('href'),
                     jQuery.proxy(waitBox, 'hide'));
            return false;
        });
        // do the same for forms
        jQuery(document).delegate('form:not([target])', 'submit', function (e) {
            var form = jQuery(this);
            // Don't make the wait box appear immediately
            waitBox.showAfter(FORM_WAIT_NO_SIGN);
            jQuery.ajax({
                url: form.attr("action"),
                data: form.serialize(),
                method: form.attr('method') || 'GET',
                contentType: form.attr('enctype') || 'application/x-www-form-urlencoded',
                success: jQuery.proxy(app, 'html'),
                complete: jQuery.proxy(waitBox, 'hide')
            });
            return false;
        });
    }
});
