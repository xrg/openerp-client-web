<table width="100%" cellpadding="0" cellspacing="0" xmlns:py="http://purl.org/kid/ns#">
    <tr>
        <td width="100%">
            <input type="hidden" name='${name}' value="${field_value}"/>
            <input type="hidden" name='${name}_domain' value="${s_domain}"/>
            <input style="width: 100%" type="text" id ='${field_id}' value="${text}" class="${field_class}" onchange="if (!this.value) document.getElementsByName('${name}')[0].value=''"/>
            <br py:if="error"/><span class="fielderror" py:if="error" py:content="error"/>
        </td>
        <td>
            <div class="spacer" />
        </td>
        <td>
        <script language="javascript">
        <!--
        	function open_win(model, id, name)
        	{
        		domain = '[]';
       			d_value = window.document.getElementsByName(name+"_"+"domain");

       			if(d_value.length>0 && d_value[0].value != '')
       			{
       				domain = d_value[0].value
       				d_value = d_value[0].value
       				temp = name.split("/");
    	    		prefix = name.replace(temp[temp.length-1],"");
        	   		d_value = d_value.replace("[(","");
    	    		d_value = d_value.replace(")]","");
        			d_value = d_value.replace("'","");
        			d_value = d_value.split(",");
        			d_name = d_value[d_value.length-1];
					value = window.document.getElementsByName(prefix + d_name);
					value = value[0].value
					if (value == '')
					value='False';
					domain = "[['" + d_name + "'," +d_value[1] + "," + value + "]]";
				}
				url = '/form/search_M2O?model='+model+'&textid='+id +'&hiddenname='+name + '&s_domain=' + domain;
        		wopen(url , 'search', 800, 600);
        	}
        -->
        </script>
            <button type="button" onclick="open_win('${relation}','${field_id}','${name}')">Select</button>
        </td>
    </tr>
</table>
