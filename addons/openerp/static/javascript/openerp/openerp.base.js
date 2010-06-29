/**
 * Opens the provided URL in the application content section.
 *
 * If the application content section (#appContent) does not
 * exist, simply change the location.
 *
 * @param url the URL to GET and insert into #appContent
 * @default afterLoad callback to execute after URL has been loaded and
 *                    inserted, if any. Takes the parameters provided
 *                    by jQuery.load: responseText, textStatus and
 *                    XMLHttpRequest
 */
var console;
// cache for the current hash url so we can know if it's changed
var currentUrl;
function openLink(url /*optional afterLoad */) {
    var app = jQuery('#appContent');
    var afterLoad = arguments[1];
    if(app.length) {
        currentUrl = url;
        window.location.hash = '#'+jQuery.param({'url': url});
        jQuery.ajax({
            url: url,
            complete: function (xhr) {
                app.html(xhr.responseText);
                if(afterLoad) { afterLoad(); }
            }
        });
    } else {
        window.location.assign(url);
    }
}
/**
 * Extract the current hash-url from the page's location
 *
 * @returns the current hash-url if any, otherwise returns `null`
 */
function hashUrl() {
    var newUrl = null;
    // would use window.location.hash but... https://bugzilla.mozilla.org/show_bug.cgi?id=483304
    var hashValue = window.location.href.split('#')[1] || '';
    jQuery.each(hashValue.split('&'), function (i, element) {
        var e = element.split("=");
        if(e[0] === 'url') {
            newUrl = decodeURIComponent(e[1]);
        }
    });
    return newUrl;
}

// Timers before displaying the wait box, in case the remote query takes too long
/** @constant */
var LINK_WAIT_NO_ACTIVITY = 300;
/** @constant */
var FORM_WAIT_NO_ACTIVITY = 500;
jQuery(document).ready(function () {
    var app = jQuery('#appContent');
    if (app.length) {
        var waitBox = new openerp.ui.WaitBox();
        // open un-targeted links in #appContent via xhr. Links with @target are considered
        // external links. Ignore hash-links.
        jQuery(document).delegate('a[href]:not([target]):not([href^="#"]):not([href^="javascript"])', 'click', function () {
            waitBox.showAfter(LINK_WAIT_NO_ACTIVITY);
            openLink(jQuery(this).attr('href'),
                     jQuery.proxy(waitBox, 'hide'));
            return false;
        });
        // do the same for forms
        jQuery(document).delegate('form:not([target])', 'submit', function () {
            var form = jQuery(this);
            form.ajaxForm();
            // Don't make the wait box appear immediately
            waitBox.showAfter(FORM_WAIT_NO_ACTIVITY);
            form.ajaxSubmit({
                complete: function (xhr) {
                    app.html(xhr.responseText);
                    waitBox.hide();
                }
            });
            return false;
        });
    }

    // wash for hash changes
    jQuery(window).bind('hashchange', function () {
        var newUrl = hashUrl();
        if(!newUrl || newUrl == currentUrl) {
            return;
        }
        openLink(newUrl);
    });
    // if the initially loaded URL had a hash-url inside
    jQuery(window).trigger('hashchange');
});

