<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python import sitetemplate ?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="sitetemplate">
<head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
    <title>${list_view.string}</title>
    <link href="/static/css/style.css" rel="stylesheet" type="text/css" />

    <script language="javascript" src="/tg_static/js/MochiKit.js"></script>
    <script language="javascript" src="/static/javascript/master.js"></script>


</head>
<body>
	<form method="post" id="view_form" name="view_form" action="/search/action">
    	<div class="view">
		    <div class="header">
    		    <div class="title">
					${list_view.string}
	        	</div>
	    		<div class="spacer"></div>
	    	</div>
    		<input type="hidden" name="terp_model" value="${model}"/>
    	    <input type="hidden" name="terp_state" value="${state}"/>
       		<input type="hidden" name="terp_ids" value="${str(ids)}"/>
	        <input type="hidden" name="terp_view_ids" value="${str(view_ids)}"/>
	        <input type="hidden" name="terp_domain" value="${str(domain)}"/>
    	    <input type="hidden" name="terp_context" value="${str(context)}"/>
      		${form.display()}
    		<div class="spacer"></div>
		    <div class="toolbar" >
        		<table>
        			<tr width = "100%">
        				<td aligh='left'>
			        		Limit
				        </td>
				        <td>
				        	<input type="text" value="80" name="limit" id="limit" algin ='left' style="width:60px" />
        				</td>
        				<td width="30px">
        				</td>
	        			<td aligh='left'>
				        	offset
				        </td>
				        <td>
			    	    	<input type="text" value="0" name="offset" id="offset" algin ='left' style="width:60px" />
        				</td>
        				<td width="100%">
	        			</td>
	        			<td>
				        	<button type="submit" name="terp_action" value='Find' title="Find Records..." >Find</button>
        				</td>
        				<td>
			    	        <button type="submit" name="terp_action" value='Cancel' title="Cancel..." >Cancel</button>
            			</td>
	            		<td>
				            <button type="button" name="terp_action" value='Ok' title="Select Record..." >Ok</button>
        	    		</td>
            		</tr>
            	</table>
            </div>
            <div class="spacer"></div>
            ${list_view.display()}
    	</div>
    </form>
</body>
</html>
