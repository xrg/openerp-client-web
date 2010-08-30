<div class="graph-block" style="text-align: center; padding: 10px; min-width: ${width}px;">

    <div id="${name}_"></div>
    
    <script type="text/javascript">
        var get_chart_${name} = function(name){
            var res = ${data|n};
            return MochiKit.Base.serializeJSON(res);
        }
    </script>
    
    <object classid="clsid:d27cdb6e-ae6d-11cf-96b8-444553540000"
            codebase="http://fpdownload.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=8,0,0,0"
            width="100%"
		    height="${height}" id="${name}" align="middle" wmode="transparent">
     
	    <param name="movie" value="${py.url('/static/ofc2/open-flash-chart.swf')}" />
	    <param name="wmode" value="transparent"/>
	    <param name="quality" value="high"/>
	    <param name="bgcolor" value="#FFFFFF"/>
	    <param name="flashvars" value="get-data=get_chart_${name}"/>
	    
	    <embed src="${py.url('/static/ofc2/open-flash-chart.swf')}"
		       width="100%"
		       height="${height}"
		       bgcolor="#FFFFFF"
		       name="${name}"
		       align="middle"
		       type="application/x-shockwave-flash"
		       pluginspage="http://www.macromedia.com/go/getflashplayer"
		       flashvars="get-data=get_chart_${name}" wmode="transparent"/>
    </object>    
    
</div>

