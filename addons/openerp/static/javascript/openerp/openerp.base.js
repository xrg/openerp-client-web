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
            error: loadingError(url),
            cache: false
        });
        return;
    }
    // Home screen
    if(jQuery('#root').length) {
        window.location.assign(
            '/?' + jQuery.param({next: url}));
        return;
    }
    window.location.assign(url);
}

/**
 * Opens the provided URL inside the application content section.
 *
 * @param url the URL to GET and insert into #appContent
 */
function openLinkFrame(url) {
    jQuery('#appContent').html(
            '<iframe src="' + url + '"></iframe>');
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
        options['scrolling'] = 'auto';
    }
    jQuery.fancybox(xhr.responseText, options);
}

/**
 * Handles errors when loading page via XHR
 * TODO: maybe we should set this as the global error handler via jQuery.ajaxSetup
 *
 * @param {String} [url] The URL to set, if any, in case of 500 error (so users can just
 * C-R or C-F5).
 */
function loadingError(url) {
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
    };
}

var ELEMENTS_WITH_CALLBACK = '[callback]:enabled:not([type="hidden"]):not([value=""]):not([readonly])';

/**
 * Performs initial triggering of all <code>onchange</code> events in form in
 * order to correctly set up initial values
 */
function initial_onchange_triggers() {
    jQuery(ELEMENTS_WITH_CALLBACK).each(function() {
        if (jQuery(this).attr('kind') == 'boolean') {
            onBooleanClicked(jQuery(this).attr('id'));
        } else {
            // We pass an arbitrary parameter to the event so we can
            // differentiate a user event from a trigger
            jQuery(this).trigger('change', [true]);
        }
    });
}
/**
 * Creates a LoadingSuccess execution for the providing app element
 * @param app the element to insert successful content in
 * @param {String} [url] the url being opened, to set as hash-url param
 */
function doLoadingSuccess(app, url) {
    return function (data, status, xhr) {
        var target;
        var active_id;
        if(xhr.getResponseHeader){
            target = xhr.getResponseHeader('X-Target');
            active_id = xhr.getResponseHeader('active_id');
        }
        if(target) {
            var _openAction;
            if (window.top.openAction) {
                _openAction = window.top.openAction;
            } else {
                _openAction = openAction;
            }
            _openAction(xhr.getResponseHeader('Location'), target, active_id);
            return;
        }
        if(url) {
            // only set url when we're actually opening the action
            jQuery.hash(url);
        }
        jQuery(window).trigger('before-appcontent-change');
        var data = xhr.responseText || data;
        if (xhr.getResponseHeader && xhr.getResponseHeader('Content-Type').match(/text\/javascript/)) {
            try {
                var parsed = jQuery.parseJSON(data);
                if (parsed.error) {
                    return error_display(parsed.error);
                }
                if (parsed.reload) {
                    if (parsed.list_grid) {
                        new ListView(parsed.list_grid).reload();
                    } else {
                        window.location.reload();
                    }
                }
            } catch(e) {
                return error_display(_('doLoadingSuccess: Cannot parse JSON'));
            }
        } else {
            jQuery(app).html(data);
        }
        jQuery(window).trigger('after-appcontent-change');

        // Only auto-call form onchanges if we're on a new object, existing
        // objects should not get their onchange callbacks called
        // automatically on edition
        if (jQuery('#_terp_id').val() == 'False') {
            initial_onchange_triggers();
        }
    };
}

/**
 * Manages navigation to actions
 *
 * @param action_url the URL of the action to open
 * @param target the target, if any, defaults to 'current'
 */
function openAction(action_url, target, terp_id) {
    var $dialogs = jQuery('.action-dialog');
    switch(target) {
        case 'new':
            jQuery.frame_dialog({
                src: action_url,
                'class': 'action-dialog'
            }, null, {
                width: 800
            });
            break;
        case 'download':
            var $form = jQuery('<form action="" target="_blank" method="POST"><input type="text" name="download" value="true"/></form>').appendTo("body");
            $form.attr("action", action_url);
            $form[0].submit();
            $form.remove();
            break;
        case 'popup':
            window.open(action_url);
            if (terp_id) {
            	window.top.editRecord(terp_id);
            }
            break;
        case 'iframe':
            openLinkFrame(action_url);
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
 * selector for delegation to links nobody handles
 */
var UNTARGETED_LINKS_SELECTOR = 'a[href]:not([target]):not([href^="#"]):not([href^="javascript"]):not([rel=external]):not([href^="http://"]):not([href^="https://"]):not([href^="//"])';

// Prevent action links from blowing up when clicked before document.ready()
jQuery(document).delegate(UNTARGETED_LINKS_SELECTOR, 'click', function (e) {
    e.preventDefault();
});
jQuery(document).ready(function () {
    // cleanup preventer
    jQuery(document).undelegate(UNTARGETED_LINKS_SELECTOR);
    var $app = jQuery('#appContent');
    if ($app.length) {
        jQuery('body').delegate(UNTARGETED_LINKS_SELECTOR, 'click', function(event){
            if (!validate_action()) {
                event.stopImmediatePropagation();
                return false;
            }
        });

        // open un-targeted links in #appContent via xhr. Links with @target are considered
        // external links. Ignore hash-links.
        jQuery(document).delegate(UNTARGETED_LINKS_SELECTOR, 'click', function () {
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
            jQuery(document).delegate(UNTARGETED_LINKS_SELECTOR, 'click', function() {
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
                    success: doLoadingSuccess(jQuery('body')),
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
            //Only autocall form onchanges when o2m open in popup.
             if (jQuery('[callback]').length){
                name = jQuery('[callback]').first().attr('id');
                var parent_prefix = name.indexOf('/') > -1 ? name.slice(0, name.lastIndexOf('/') + 1) : '';
                if (parent_prefix != ''){
                    if(jQuery(idSelector(parent_prefix + '_terp_id')).val() == 'False'){
                        initial_onchange_triggers();
                    }
                }
            }
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
    var $caller = jQuery(ELEMENTS_WITH_CALLBACK);
    $caller.each(function(){
        if (!jQuery(this).val()) {
            if (jQuery(this).attr('kind') == 'boolean') {
                onBooleanClicked(jQuery(this).attr('id'));
            }
            else {
                jQuery(this).change();
            }
        }
    });
});

// Hook onchange for all elements
jQuery(document).delegate('[callback], [change_default]', 'change', function () {
    if (jQuery(this).is(':input.checkbox:enabled')
            || !jQuery(this).is(':input')
            || !window.onChange) {
        return;
    }
    onChange(this);
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
            jQuery('#' + model.replace(/\./g, '-') + '-' + id)
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
        $loader.text($loader.text().replace(/(\.*)(\s)(\s*)$/, '$1.$3'));
    }
    LOADER_THROBBER = setTimeout(loader_throb, THROBBER_DELAY);
}
jQuery(document).bind({
    ajaxStart: function() {
        var $loader = jQuery('#ajax_loading');
        if(!$loader.length) {
            $loader = jQuery('<div id="ajax_loading">'
                             + _('Loading')
                             + '&nbsp;&nbsp;&nbsp;</div>'
            ).appendTo(document.body);
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
        if(!xhr) return;
        var concurrencyInfo = xhr.getResponseHeader('X-Concurrency-Info');
        if(!concurrencyInfo) return;
        updateConcurrencyInfo(jQuery.parseJSON(concurrencyInfo));

    }
});
