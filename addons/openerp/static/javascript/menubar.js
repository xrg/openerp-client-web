
function adjustAppFrame(evt){

    var $ = jQuery;
   
    var h = $("#appFrame").contents().find("body").height();
    var w = $("#appFrame").contents().width();
    
    $("#menubar").width();
    $("#appFrame").height(Math.max(0, h));
        
    var mh = $("#menubar").height();
    var ww = $(window).width();
    var tw = $("#menubar").width() + w;
    var rw = ww - $("#menubar").width();
    
    var w = tw > ww ? w : rw - 16;
    
    $("#appFrame").width(Math.max(0, w));    
    $("table#contents").height(Math.max(h, mh));
}

