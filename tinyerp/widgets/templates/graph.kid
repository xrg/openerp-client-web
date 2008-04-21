<span xmlns:py="http://purl.org/kid/ns#">
	<table width="100%">
	    <tr>
	        <td align="center">
	        	<div id="my_chart"/>
	        	<img class="graph" src="${tg.query('/graph', 
	        							_terp_model=model, 
	        							_terp_view_id=view_id, 
	        							_terp_ids=ustr(ids), 
	        							_terp_domain=ustr(domain), 
	        							_terp_context=ustr(context),
	        							 width=width, 
	        							 height=height)}"> </img>
	        </td>
	    </tr>
	</table>
	<script type="text/javascript">
			
			var so = new SWFObject("/static/open-flash-chart.swf", "ofc", "450", "300", "9", "#FFFFFF");
	    	so.addVariable("data", "${tg.quote_plus(tg.query('/graph/bar_chart', _terp_model=model, _terp_view_id=view_id, _terp_ids=ustr(ids), _terp_domain=ustr(domain), _terp_context=ustr(context), width=width, height=height))}");		
	    	
	    	so.write("my_chart");
	 	
	</script>
</span>