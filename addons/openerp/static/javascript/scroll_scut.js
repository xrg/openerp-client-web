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
// -   All names, links and logos of Tiny, Open ERP and Axelor must be 
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

$ = jQuery;

$(function(){
	//Get our elements for faster access and set overlay width
	var div = $('div.sc_menu'),
	             ul = $('ul.sc_menu');
	
	var ulWidth = 0;
	$('ul.sc_menu li.menu_tabs').each(function(i){
	    ulWidth += $(this).outerWidth();
	});
	
	ulWidth = ulWidth + 10;
	
	$(ul).css('width', ulWidth + 'px');
	
	//Get menu width
	var divWidth = div.width();
	
	$('#scroll_left').mouseover(function(){
		if (divWidth < ulWidth) {
			wd = ulWidth-divWidth;
			if (wd < 30 ) {
				$("ul.sc_menu").animate({"left": "-=" + wd + "px"}, "slow");
				ulWidth = ulWidth - wd;
			}
			else {
				$("ul.sc_menu").animate({"left": "-=30px"}, "slow");
				ulWidth = ulWidth - 30;
			}
		}
	});
	
	$('#scroll_right').mouseover(function(){
		var left_css = $("ul.sc_menu").css('left');
		left_css = parseInt(left_css.split('px')[0]);
		if (left_css != 0 || left_css < 0) {
			if (left_css > -30) {
				$("ul.sc_menu").animate({"left": "-=" + left_css + "px"}, "slow");
				ulWidth = ulWidth - left_css;
			}
			else {			
				$("ul.sc_menu").animate({"left": "+=30px"}, "slow");
				ulWidth = ulWidth + 30;
			}
		}
	});
});

