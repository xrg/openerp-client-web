/*
CSS Browser Selector v0.4.0 (Nov 02, 2010)
Rafael Lima (http://rafael.adm.br)
http://rafael.adm.br/css_browser_selector
License: http://creativecommons.org/licenses/by/2.5/
Contributors: http://rafael.adm.br/css_browser_selector#contributors
*/
function css_browser_selector(u){var ua=u.toLowerCase(),is=function(t){return ua.indexOf(t)>-1},g='gecko',w='webkit',s='safari',o='opera',m='mobile',h=document.documentElement,b=[(!(/opera|webtv/i.test(ua))&&/msie\s(\d)/.test(ua))?('ie ie'+RegExp.$1):is('firefox/2')?g+' ff2':is('firefox/3.5')?g+' ff3 ff3_5':is('firefox/3.6')?g+' ff3 ff3_6':is('firefox/3')?g+' ff3':is('gecko/')?g:is('opera')?o+(/version\/(\d+)/.test(ua)?' '+o+RegExp.$1:(/opera(\s|\/)(\d+)/.test(ua)?' '+o+RegExp.$2:'')):is('konqueror')?'konqueror':is('blackberry')?m+' blackberry':is('android')?m+' android':is('chrome')?w+' chrome':is('iron')?w+' iron':is('applewebkit/')?w+' '+s+(/version\/(\d+)/.test(ua)?' '+s+RegExp.$1:''):is('mozilla/')?g:'',is('j2me')?m+' j2me':is('iphone')?m+' iphone':is('ipod')?m+' ipod':is('ipad')?m+' ipad':is('mac')?'mac':is('darwin')?'mac':is('webtv')?'webtv':is('win')?'win'+(is('windows nt 6.0')?' vista':''):is('freebsd')?'freebsd':(is('x11')||is('linux'))?'linux':'','js']; var c = b.join(' '); h.className += ' '+c; return c;} css_browser_selector(navigator.userAgent);

var $ = jQuery;
/**
 * Compact labels plugin
 */
(function($){$.fn.compactize=function(){return this.each(function(){var label=$(this),input=$('#'+label.attr('for'));input.focus(function(){label.hide();}).blur(function(){if(input.val()===''){label.show();}});window.setTimeout(function(){if(input.val()!==''){label.hide();}},50);});};})(jQuery);

/*
 * hrefID jQuery extention - returns a valid #hash string from link href attribute in Internet Explorer
 */
(function($){$.fn.extend({hrefId:function(){return $(this).attr('href').substr($(this).attr('href').indexOf('#'));}});})(jQuery);

/*
 * Scripts
 *
 */
jQuery(function($) {
 
	var Engine = {
		utils : {
			links : function(){
				$('a[rel*=external]').click(function(e){
					e.preventDefault();
					window.open($(this).attr('href'));						  
				});
			},
			mails : function(){
				$('a[href^=mailto:]').each(function(){
					var mail = $(this).attr('href').replace('mailto:','');
					var replaced = mail.replace('/at/','@');
					$(this).attr('href','mailto:'+replaced);
					if($(this).text() == mail) {
						$(this).text(replaced);
					}
				});
			}
		}
	};

	Engine.utils.links();
	Engine.utils.mails();
	
});
