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
    var $app = jQuery('#appContent');
    var afterLoad = arguments[1];
    if($app.length) {
        currentUrl = url;
        window.location.href = '#'+jQuery.param({'url': url});
        jQuery.ajax({
            url: url,
            complete: function () {
                if(afterLoad) { afterLoad(); }
            },
            success: doLoadingSuccess($app[0]),
            error: loadingError
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
        showCloseButton: true,
        overlayOpacity: 0.7
    };
    if(xhr.getResponseHeader('X-Maintenance-Error')) {
        options['autoDimensions'] = false;
    }
    jQuery.fancybox(xhr.responseText, options);
}

/**
 * Handles errors when loading page via XHR
 * TODO: maybe we should set this as the global error handler via jQuery.ajaxSetup
 *
 * @param xhr The XHR object
 */
function loadingError(xhr) {
    switch (xhr.status) {
        case 500:
            displayErrorOverlay(xhr);
            break;
        case 401: // Redirect to login, probably
            window.location.assign(
                xhr.getResponseHeader('Location'));
            break;
        default:
            if(window.console) {
                console.warn("Failed to load ", xhr.url, ":", xhr.status, xhr.statusText);
            }
    }
}

/**
 * Creates a LoadingSuccess execution for the providing app element
 * @param app the element to insert successful content in
 */
function doLoadingSuccess(app) {
    return function (data, status, xhr) {
        var action_url = xhr.getResponseHeader('Location');
        var target = xhr.getResponseHeader('X-Target');
        if(target) {
            window.top.openAction(action_url, target);
            return;
        }
        jQuery(window).trigger('before-appcontent-change');
        jQuery(app).html(xhr.responseText || data);
        jQuery(window).trigger('after-appcontent-change');
    }
}

/**
 * Manages navigation to actions
 *
 * @param action_url the URL of the action to open
 * @param target the target, if any, defaults to 'current'
 */
function openAction(action_url, target) {
    var $dialogs = jQuery('.action-dialog');
    switch(target) {
        case 'new':
            var $contentFrame = jQuery('<iframe>', {
                src: action_url,
                frameborder: 0,
                width: '99%',
                height: '99%'
            });
            jQuery('<div class="action-dialog">')
                .appendTo(document.documentElement)
                .dialog({
                    modal: true,
                    width: 640,
                    height: 480,
                    close: function () {
                        var $this = jQuery(this);
                        $this.find('iframe').remove();
                        setTimeout(function () {
                            $this.dialog('destroy').remove();
                        });
                    }
                })
                .append($contentFrame);
            break;
        case 'current':
        default:
            openLink(action_url);
    }
    $dialogs.dialog('close');
}
function closeAction() {
    jQuery('.action-dialog').dialog('close');
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
        jQuery('body').delegate('a[href]:not([target="_blank"]):not([href^="#"]):not([href^="javascript"]):not([rel=external])', 'click', function(){
            validate_action();
        });

        // open un-targeted links in #appContent via xhr. Links with @target are considered
        // external links. Ignore hash-links.
        jQuery(document).delegate('a[href]:not([target]):not([href^="#"]):not([href^="javascript"]):not([rel=external])', 'click', function () {
            openLink(jQuery(this).attr('href'));
            return false;
        });
        // do the same for forms
        jQuery(document).delegate('form:not([target])', 'submit', function () {
            var $form = jQuery(this);
            $form.ajaxSubmit({
                data: {'requested_with': 'XMLHttpRequest'},
                success: doLoadingSuccess($app[0]),
                error: loadingError
            });
            return false;
        });
    } else {
        if(jQuery(document).find('div#root').length) {
            jQuery(document).delegate('a[href]:not([target]):not([href^="#"]):not([href^="javascript"]):not([rel=external])', 'click', function() {
                window.location.href = openobject.http.getURL('/openerp', {
                    'next': jQuery(this).attr('href')
                });
                return false;
            });
        }
        // For popup like o2m submit actions.
        else {
            jQuery(document).delegate('form#view_form:not([target])', 'submit', function () {
                var $form = jQuery('#view_form');
                // Make the wait box appear immediately
                $form.ajaxSubmit({
                    data: {'requested_with': 'XMLHttpRequest'},
                    success: doLoadingSuccess(jQuery('table.view')[0]),
                    error: loadingError
                });
                return false;
            });
        }
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
jQuery(document).delegate(
        'input.checkbox:enabled:not(.grid-record-selector)',
        'click', function () {
    if(window.onBooleanClicked) {
        onBooleanClicked(jQuery(this).attr('id').replace(/_checkbox_$/, ''));
    }
});

jQuery(document).bind('ready ajaxStop', function (){
    var $caller = jQuery('[callback]:not([type="hidden"]):not([value=""]):not([disabled]):not([readonly]))');
    $caller.each(function(){
        if (jQuery(this).attr('kind') == 'boolean') {
            onBooleanClicked(jQuery(this).attr('id'));
        } else {
            jQuery(this).change();
        }
    });
});

// Hook onchange for all elements
jQuery(document).delegate('[callback], [onchange_default]', 'change', function () {
    if(window.onChange && !jQuery(this).is(':input.checkbox:enabled')) {
        onChange(this);
    }
});

/**
 * Updates existing concurrency info with the data provided
 * @param info a map of {model: {id: concurrency info}} serialized into the existing concurrency info inputs
 */
function updateConcurrencyInfo(info) {
    jQuery.each(info, function (model, model_data) {
        jQuery.each(model_data, function (id, concurrency_data) {
            var formatted_key = "'" + model + ',' + id + "'";
            var formatted_concurrency_value = (
                    "(" + formatted_key + ", " +
                            "'" + concurrency_data + "'" +
                            ")"
                    );
            jQuery('#' + model.replace('.', '-') + '-' + id)
                    .val(formatted_concurrency_value);
        });
    });
}

var LOADER_THROBBER;
var THROBBER_DELAY = 300;
function loader_throb() {
    var $loader = jQuery('#ajax_loading');
    if(/\.{3}$/.test($loader.text())) {
        // if we have three dots, reset to three nbsp
        $loader.html($loader.text().replace(/\.{3}$/, '&nbsp;&nbsp;&nbsp;'));
    } else {
        // otherwise replace first space with a dot
        $loader.text($loader.text().replace(/(\.*)(\s)(\s*)$/, '$1.$3'))
    }
    LOADER_THROBBER = setTimeout(loader_throb, THROBBER_DELAY);
}
jQuery(document).bind({
    ajaxStart: function() {
        var $loader = jQuery('#ajax_loading');
        if(!$loader.length) {
            $loader = jQuery('<div id="ajax_loading">Loading&nbsp;&nbsp;&nbsp;</div>').appendTo(document.body);
        }
        $loader.css({
            left: (jQuery(window).width() - $loader.outerWidth()) / 2
        }).show();
        loader_throb();
    },
    ajaxStop: function () {
        clearTimeout(LOADER_THROBBER);
        jQuery('#ajax_loading').hide();
    },
    ajaxComplete: function (e, xhr) {
        var concurrencyInfo = xhr.getResponseHeader('X-Concurrency-Info');
        if(!concurrencyInfo) return;
        updateConcurrencyInfo(jQuery.parseJSON(concurrencyInfo));

    }
});
