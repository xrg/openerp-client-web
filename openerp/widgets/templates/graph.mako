<div class="graph-block" style="text-align: center; padding: 10px; min-width: $width">
    <object classid="clsid:d27cdb6e-ae6d-11cf-96b8-444553540000"
            codebase="http://fpdownload.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=8,0,0,0"
            width="${width}" 
            height="${height}" 
            id="${name}" 
            align="middle">

	    <param name="allowScriptAccess" value="sameDomain" />
	    <param name="movie" value="open-flash-chart.swf" />
	    <param name="quality" value="high" />

	    <embed src="/static/open-flash-chart.swf"
		       quality="high"
		       bgcolor="#FFFFFF"
		       width="${width}"
		       height="${height}"
		       name="${name}"
		       align="middle"
		       allowScriptAccess="sameDomain"
		       type="application/x-shockwave-flash"
		       pluginspage="http://www.macromedia.com/go/getflashplayer"
               flashvars="data-file=${url}"/>
    </object>
</div>

