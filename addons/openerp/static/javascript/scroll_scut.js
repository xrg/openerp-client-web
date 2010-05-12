$ = jQuery;

$(function(){
	//Get our elements for faster access and set overlay width
	var div = $('div.sc_menu'),
	             ul = $('ul.sc_menu');
	
	var ulWidth = 0;
	jQuery('ul.sc_menu li.menu_tabs').each(function(i){
	    ulWidth += $(this).outerWidth();
	});
	
	ulWidth = ulWidth + 10;
	
	$(ul).css('width', ulWidth + 'px');
	
	//Get menu width
	var divWidth = div.width();
	
	$('#scroll_left').click(function(){
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
	
	$('#scroll_right').click(function(){
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

