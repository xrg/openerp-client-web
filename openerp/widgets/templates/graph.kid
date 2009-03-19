<table width="100%" xmlns:py="http://purl.org/kid/ns#" class="graph-table">
    <tr>
        <td align="center">
        	
			<div class="graph" id="${chart_name}" style="width: ${width}; height: ${height}; min-width: 350px; min-height: 350px;"></div>
			
			<script type="text/javascript">
				var model = "${model}";
				var view_id = "${view_id}";
				var ids = "${ustr(ids)}";
				var domain = "${ustr(domain)}";
				var context = "${ustr(context)}";
				
				var chart = '${chart_type}';
				
				var address = urlEncode("/graph/"+chart+"?_terp_model="+model+"&amp;_terp_view_id="+view_id+"&amp;_terp_ids="+ids+"&amp;_terp_domain="+domain+"&amp;_terp_context="+context); 
				
            	swfobject.embedSWF("/static/open-flash-chart.swf", "${chart_name}", "500", "350", "9.0.0", "expressInstall.swf", 
            							{"data-file": address});
            											
            </script>
			
            <script type="text/javascript">
            
            	if (getElement('_terp_model').value == '${model}' &amp;&amp; '${chart_type}'=='bar') {
            	 
            	 	var make_div = DIV({'id': 'make_resize', 'style': 'width: 100%; height: ${height};'});
            	    var graph_div = DIV({'class': 'graph', 'style': 'width: 100%; height: 99%;'});
            	    var resize_div = DIV({'class':'chart_resize'});
            	    
            	    MochiKit.DOM.appendChildNodes(make_div, graph_div);
            	    MochiKit.DOM.appendChildNodes(make_div, resize_div);
            	    
            	    MochiKit.DOM.swapDOM('${chart_name}', make_div);
            	    
            	    graph_div.id = '${chart_name}';
            	    
	        		resize = new MochiKit.DragAndDrop.Resizable('make_resize', {
		            	constraint: 'vertical',
		            	handle: 'chart_resize'
	        		});
	        		
	        		connect(MochiKit.DragAndDrop.Resizables, 'onStart', function(evt) {
	        				MochiKit.DOM.hideElement('swf_'+'${chart_name}');
	        		});
	        		connect(MochiKit.DragAndDrop.Resizables, 'onEnd', function(evt){
	        				MochiKit.DOM.showElement('swf_'+'${chart_name}');
	        		});
				}
        		
        	</script>
            
        </td>
    </tr>
</table>