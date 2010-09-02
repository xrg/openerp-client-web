// cache for the current hash url so we can know if it's changed
var currentUrl;
/**
 * Opens the provided URL in the application content section.
 *
 * If the application content section (#appContent) does not
 * exist, simply change the location.
 *
 * @param url the URL to GET and insert into #appContent
 * @default afterLoad callback to execute after URL has been loaded and
 *                    inserted, if any.
 */
function openLink(url /*optional afterLoad */) {
    var app = jQuery('#appContent');
    var afterLoad = arguments[1];
    if(app.length) {
        currentUrl = url;
        window.location.hash = '#'+jQuery.param({'url': url});
        jQuery.ajax({
            url: url,
            complete: function () {
                if(afterLoad) { afterLoad(); }
            },
            success: doLoadingSuccess(app),
            error: function (xhr, status, error) {
                if(xhr.status != 500) {
                    if(window.console) {
                        console.warn("Failed to load ", url, ":", status, error);
                    }
                    return;
                }
                displayErrorOverlay(xhr);
            }
        });
    } else {
        window.location.assign(url);
    }
}
/**
 * Displays a fancybox containing the error display
 * @param xhr the received XMLHttpResponse
 */
function displayErrorOverlay(xhr) {
    var options = {
        showCloseButton: false,
        overlayOpacity: 0.7
    };
    if(xhr.getResponseHeader('X-Maintenance-Error')) {
        options['autoDimensions'] = false;
        options['showCloseButton'] = true;
    }
    jQuery.fancybox(xhr.responseText, options);
}

/**
 * Creates a LoadingSuccess execution for the providing app element
 * @param app the element to insert successful content in
 */
function doLoadingSuccess(app) {
    return function (data, status, xhr) {
        jQuery(window).trigger('before-appcontent-change');
        jQuery(app).html(xhr.responseText);
        jQuery(window).trigger('after-appcontent-change');
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
    var $app = jQuery('#appContent');
    if ($app.length) {
        var waitBox = new openerp.ui.WaitBox();
        // open un-targeted links in #appContent via xhr. Links with @target are considered
        // external links. Ignore hash-links.
        jQuery(document).delegate('a[href]:not([target]):not([href^="#"]):not([href^="javascript"]):not([rel=external])', 'click', function () {
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
                complete: jQuery.proxy(waitBox, 'hide'),
                success: doLoadingSuccess($app),
                error: function (xhr, status, error) {
                    if(xhr.status != 500) {
                        if(window.console) {
                            console.warn("Failed to load ", form.attr('method') || 'GET', form.attr('action'), ":", status, error);
                        }
                        return;
                    }
                    displayErrorOverlay(xhr);
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

// Hook onclick for boolean alteration propagation
var onBooleanClicked;
jQuery(document).delegate(
        'input.checkbox:enabled:not(.grid-record-selector)',
        'click', function () {
    if(onBooleanClicked) {
        onBooleanClicked(jQuery(this).attr('id').replace(/_checkbox_$/, ''));
    }
});
// Hook onchange for all elements
var onChange;
jQuery(document).delegate('[callback], [onchange_default]', 'change', function () {
    if(onChange && !jQuery(this).is(':input.checkbox:enabled')) {
        onChange(this);
    }
});
