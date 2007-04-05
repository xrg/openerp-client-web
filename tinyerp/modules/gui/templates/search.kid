<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python import sitetemplate ?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="sitetemplate">
<head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
    <title>Search ${list_view.string}</title>
    <link href="/static/css/style.css" rel="stylesheet" type="text/css" />

    <script language="javascript" src="/tg_static/js/MochiKit.js"></script>
    <script language="javascript" src="/static/javascript/master.js"></script>

    <script language="javascript">
    <!--
        function submit_form(action){
            form = $('search_form');
            form.action = '/search/' + action;
            form.submit();
        }

        function setfield(model, textid, hiddenname)
        {
        	boxes = window.document.getElementsByName('check');
        	if (boxes.length > 0)
        	{
        		for(i=0;i<=boxes.length;i++)
        		{
        			if (boxes[i].checked)
        			{
        				id = window.document.getElementsByName('check')[i].value

						function settext(xmlhttp)
        				{
				        	data = evalJSONRequest(xmlhttp);
				        	window.opener.document.getElementsByName(hiddenname)[0].value = id;
				        	window.opener.document.getElementById(textid).value = data['name'];
				        	close_form();
				        }

				        function errtext(err)
				        {
				        	alert("error" + err);
				        }

        				d=doSimpleXMLHttpRequest("/search/get_string",{'model':model, 'id':id});
        				d.addCallbacks(settext,errtext);
						break;
					}
				}
			}
        }

        function close_form()
        {
        	close();
        }
    -->
    </script>
</head>

<body>
	<form method="post" id="search_form" name="search_form" action="/search/ok">
    	<div class="view">
		    <div class="header">
    		    <div class="title">Search ${list_view.string}</div>
    		    <div class="spacer"></div>
	    	</div>
    	    <input type="hidden" name="_terp_model" value="${model}"/>
	        <input type="hidden" name="_terp_state" value="${state}"/>
	        <input type="hidden" name="_terp_id" value="${str(id)}"/>
        	<input type="hidden" name="_terp_view_ids" value="${str(view_ids)}"/>
       		<input type="hidden" name="_terp_view_mode" value="${str(view_mode)}"/>
       		<input type="hidden" name="_terp_view_mode2" value="${str(view_mode2)}"/>
	        <input type="hidden" name="_terp_domain" value="${str(domain)}"/>
    	    <input type="hidden" name="_terp_context" value="${str(context)}"/>
    	    <input type="hidden" name="_terp_fields_type" value="${str(form_view.fields_type)}"/>
    	    <input type="hidden" name="_terp_textid" value="${textid}" py:if="textid"/>
    	    <input type="hidden" name="_terp_hiddenname" value="${hiddenname}" py:if="hiddenname"/>
			<input type="hidden" name="_terp_s_domain" value="${s_domain}" py:if="s_domain"/>



      		${form_view.display()}
    		<div class="spacer"></div>
		    <div class="toolbar">
        		<table>
        			<tr width = "100%">
        				<td aligh='left'>Limit</td>
				        <td>
				            <input type="text" value="80" name="limit" id="limit" algin ='left' style="width:60px" />
        				</td>

        				<td width="30px"></td>

	        			<td aligh='left'>Offset</td>
				        <td>
			    	    	<input type="text" value="0" name="offset" id="offset" algin ='left' style="width:60px" />
        				</td>

        				<td width="100%"></td>

	        			<td>
				        	<button type="button" title="Find Records..." onclick="submit_form('find')">Find</button>
        				</td>
        				<td py:if="not textid">
			    	        <button type="button" title="Cancel..." onclick="submit_form('cancel')">Cancel</button>
            			</td>
            			<td py:if="textid">
			    	        <button type="button" title="Cancel..." onclick="close_form()">Cancel</button>
            			</td>

	            		<td py:if="not textid">
	            			${textid}
				            <button type="button" title="Select Record..." onclick="submit_form('ok')">Ok</button>
        	    		</td>
        	    		<td py:if="textid">
				            <button type="button" title="Select Record..." onclick="setfield('${model}', '${textid}','${hiddenname}')">Ok</button>
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
