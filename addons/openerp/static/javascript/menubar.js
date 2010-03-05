
var adjustAppFrame = function(evt){

    var $ = jQuery;
    
    var h = $("#appFrame").contents().find("body").height();
    var w = $("#appFrame").contents().find("body").width();
    
    $("#appFrame").height(h);
        
    var mh = $("#menubar").height();
    var ww = $(window).width();
    var tw = $("#menubar").width() + w;
    
    $("#header, #footer").width(Math.max(tw, ww));
    
    $("table#contents").height(Math.max(h, mh));
}

