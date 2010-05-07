jQuery(document).ready(function () {
    var app = jQuery('#appContent');
    if (app.length) {
        // open un-targeted links in #appContent via xhr. Links with @target are considered
        // external links
        jQuery(document).delegate('a[href]:not([target])', 'click', function (e) {
            app.load(jQuery(this).attr('href'));
            return false;
        });
        // do the same for forms
        jQuery(document).delegate('form:not([target])', 'submit', function (e) {
            var form = jQuery(this);
            jQuery.ajax({
                url: form.attr("action"),
                data: form.serialize(),
                method: form.attr('method') || 'GET',
                contentType: form.attr('enctype') || 'application/x-www-form-urlencoded',
                success: jQuery.proxy(app, 'html')
            });
            return false;
        });
    }
});
