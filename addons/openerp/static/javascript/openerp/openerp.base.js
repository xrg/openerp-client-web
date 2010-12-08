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
        jQuery.ajax({
            url: url,
            complete: function () {
                if(afterLoad) { afterLoad(); }
            },
            success: doLoadingSuccess($app[0], url),
            error: loadingError(url)
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
        overlayOpacity: 0.7,
        scrolling: 'no'
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
 * @param url The URL to set, if any, in case of 500 error (so users can just
 * C-R or C-F5).
 */
function loadingError(/*url*/) {
    var url;
    if(arguments[0]) {
        url = arguments[0]
    }
    return function (xhr) {
        if(url) { $.hash(url); }
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
}

/**
 * Creates a LoadingSuccess execution for the providing app element
 * @param app the element to insert successful content in
 * @param url the url being opened, to set as hash-url param
 */
function doLoadingSuccess(app/*, url*/) {
    var url;
    if(arguments[1]) {
        url = arguments[1];
    }
    return function (data, status, xhr) {
        var target = xhr.getResponseHeader('X-Target');
        if(target) {
            var _openAction;
            if (window.top.openAction) {
                _openAction = window.top.openAction;
            } else {
                _openAction = openAction;
            }
            _openAction(xhr.getResponseHeader('Location'), target);
            return;
        }
        if(url) {
            // only set url when we're actually opening the action
            $.hash(url);
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
            jQuery('<iframe>', {
                src: action_url,
                'class': 'action-dialog',
                frameborder: 0
            }).appendTo(document.documentElement)
                .dialog({
                    modal: true,
                    width: 640,
                    height: 480,
                    close: function () {
                        jQuery(this).dialog('destroy').remove();
                    }
                });
            break;
        case 'popup':
            window.open(action_url);
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
                error: loadingError()
            });
            return false;
        });
    } else {
        if(jQuery(document).find('div#root').length) {
            jQuery(document).delegate('a[href]:not([target]):not([href^="#"]):not([href^="javascript"]):not([rel=external])', 'click', function() {
                jQuery.ajax({
                    url: jQuery(this).attr('href'),
                    success: doLoadingSuccess(jQuery(this).attr('href'))
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
                    error: loadingError()
                });
                return false;
            });
        }
    }

    // wash for hash changes
    jQuery(window).bind('hashchange', function () {
        var newUrl = $.hash();
        if(!newUrl || newUrl == $.hash.currentUrl) {
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

jQuery(document).bind('ready', function (){
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
