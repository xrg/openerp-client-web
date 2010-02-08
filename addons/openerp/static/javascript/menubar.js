
(function() {

var menubar, appbar, menuTab = null
var nHeader, nFooter = 0;
var static_tabs = 0;

var onWindowResize = function(evt) {

    var dim = getViewportDimensions();
    
    var h = dim.h - nHeader - 4 - 2 - static_tabs + 'px';
    var w = dim.w - 16 + 'px';
    
    if (menubar) {
	    with (menubar.style) {
	        height = h;
	    }
    }
    
    if (appbar) {
    	with (appbar.style) {
	        height = h;
	    }
    }
    
    if (menuTab) {
    	with (menuTab.style) {
    		width = w;
    	}
    }
}

MochiKit.Signal.connect(window, "onresize", onWindowResize);
MochiKit.DOM.addLoadEvent(function(evt){

    menubar = getElement("menubar_container");
    appbar = getElement("app_container");
    menuTab = getElement("static_menu_tabs");
    
    nHeader = getElementDimensions("header").h;
    static_tabs = getElementDimensions("static_menu_tabs").h;
    
    onWindowResize();
});

})()
