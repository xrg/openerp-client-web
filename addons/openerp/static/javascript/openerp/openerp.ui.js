////////////////////////////////////////////////////////////////////////////////
//
// Copyright (C) 2007-TODAY Tiny ERP Pvt Ltd. All Rights Reserved.
//
// $Id$
//
// Developed by Tiny (http://openerp.com) and Axelor (http://axelor.com).
//
// The OpenERP web client is distributed under the "OpenERP Public License".
// It's based on Mozilla Public License Version (MPL) 1.1 with following 
// restrictions:
//
// -   All names, links and logos of Tiny, OpenERP and Axelor must be 
//     kept as in original distribution without any changes in all software 
//     screens, especially in start-up page and the software header, even if 
//     the application source code has been changed or updated or code has been 
//     added.
//
// -   All distributions of the software must keep source code with OEPL.
// 
// -   All integrations to any other software must keep source code with OEPL.
//
// If you need commercial licence to remove this kind of restriction please
// contact us.
//
// You can see the MPL licence at: http://www.mozilla.org/MPL/MPL-1.1.html
//
////////////////////////////////////////////////////////////////////////////////

var openobject;
if (!openobject && !openobject.dom) {
    throw "openobject.dom is required by 'openerp.ui'.";
}
var openerp;
if (!openerp) {
    openerp = {};
}

openerp.ui = {};

function toggle_sidebar() {
    function a() {
        jQuery('#tertiary').toggleClass('sidebar-open sidebar-closed');
    }
    if (typeof(Notebook) == "undefined") {
        a();
    } else {
        Notebook.adjustSize(a);
    }
	adjustTopWidth();
    
}

function adjustTopWidth() {
	var docWidth = jQuery(document).width();
	var accordionWidth = jQuery('#secondary').width();
	var formWidth;
	var formHeight;
	var $form = jQuery('#appContent table:first');
	
	if(!$form.get().length) {
		$form = jQuery('#appContent');
	}
	
	formWidth = $form.width();
	formHeight = $form.height();
	
	var toggle_accordion_width = jQuery('#toggle_accordion').width();
	var totalWidth = accordionWidth + toggle_accordion_width + formWidth;
	var setWidth;
	
	if(totalWidth < docWidth) setWidth = totalWidth;
	else setWidth = docWidth;
	
	jQuery('div#top, #main_nav').width(setWidth);
	var logoWidth = jQuery('p#cmp_logo').outerWidth();
    var shortcuts = jQuery('#shortcuts');
    var offset = shortcuts.outerWidth() - shortcuts.width();
    shortcuts.css('width', setWidth - logoWidth - offset);
    
    var accordionHeight = jQuery('#secondary div.wrap').height();
	if(accordionHeight > formHeight) {
    	jQuery('#secondary, #toggle_accordion').height(accordionHeight);
    	$form.height(accordionHeight);
    	
    	if(!window.browser.isGecko) {
	    	var countWidth = docWidth - totalWidth;
	    	
	    	if(countWidth > 0)
	    		$form.width(formWidth - toggle_accordion_width);
	    		
			else if(countWidth < 0) {
				countWidth = countWidth * -1;
				$form.width(formWidth - countWidth - toggle_accordion_width);
			}
    	}
    }
    
	else {
		jQuery('#secondary, #toggle_accordion').height(formHeight);	
	}
	jQuery('#footer_section').width(setWidth);
    jQuery('#footer_section').show();
    
}

jQuery(document).bind('shortcuts-alter', function () {
    var shortcuts = jQuery('#shortcuts > ul');
    var shortcuts_row = jQuery('#shortcuts');
    if(!shortcuts.length) { return; }
    var totalWidth = shortcuts.get(0).scrollWidth;
    var visibleWidth = shortcuts.outerWidth();

    if(totalWidth > visibleWidth) {
        if (!shortcuts_row.hasClass('scrolling')) {
            shortcuts_row.addClass('scrolling');
        }
        /*
            When resizing the window, if the bar is scrolled far to the right,
            we're going to display emptiness on the right even though we have hidden content on the left.
            Unscroll to fix that.
         */
        if(shortcuts.scrollLeft() > (totalWidth - visibleWidth)) {
            shortcuts.scrollLeft(totalWidth - visibleWidth);
        }
    } else {
        if(shortcuts_row.hasClass('scrolling')) {
            shortcuts_row.removeClass('scrolling');
            shortcuts.scrollLeft(0);
        }
    }
    setRowWidth();
});

// trigger on window load so all other handlers (including resizer) have executed
// further stuff will be handled when adding/removing shortcuts anyway (theoretically)
jQuery(window).load(function () {
    var shortcuts = jQuery('#shortcuts');
    var scrolling_left, scrolling_right;
    var scroll_left = jQuery('<div id="shortcuts-scroll-left" class="scroller">').hover(
        function () {
            var scrollable = shortcuts.children('ul');
            scrolling_left = setInterval(function () {
                if(scrollable.scrollLeft() == 0) {
                    clearInterval(scrolling_left);
                }
                scrollable.scrollLeft(scrollable.scrollLeft() - 3);
            }, 30);
        }, function () {
            clearInterval(scrolling_left);
    });
    var scroll_right = jQuery('<div id="shortcuts-scroll-right" class="scroller">').hover(
        function () {
            var scrollable = shortcuts.children('ul');
            scrolling_right = setInterval(function () {
                if((scrollable.scrollLeft() + scrollable.outerWidth()) == scrollable.get(0).scrollWidth) {
                    clearInterval(scrolling_right);
                }
                scrollable.scrollLeft(scrollable.scrollLeft() + 3);
            }, 30);
        }, function () {
            clearInterval(scrolling_right);
    });
    shortcuts.prepend(scroll_right).prepend(scroll_left);
    jQuery(document).trigger('shortcuts-alter');
    jQuery(window).resize(function () {
        jQuery(document).trigger('shortcuts-alter');
    })
});
