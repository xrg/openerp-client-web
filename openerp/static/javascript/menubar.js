
(function() {

var menubar, appbar = null
var nHeader, nFooter = 0;

var onWindowResize = function(evt) {

    var dim = getViewportDimensions();
    var h = dim.h - nHeader - 4 - 2 + 'px';
    
    with (menubar.style) {
        height = h;
    }
    
    with (appbar.style) {
        height = h;
    }
    
}

MochiKit.Signal.connect(window, "onresize", onWindowResize);
MochiKit.DOM.addLoadEvent(function(evt){

    menubar = openobject.dom.get("menubar_container");
    appbar = openobject.dom.get("app_container");
    
    nHeader = getElementDimensions("header").h;
    
    onWindowResize();
});

})()
