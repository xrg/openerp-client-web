<span xmlns:py="http://purl.org/kid/ns#">
	<table width="100%">
		<tr>
			<td width="100%">
			    <input type="text" kind="${kind}" name='${name}' id ='${field_id}' style="width :100%" value="${value}" class="${field_class}" py:attrs="attrs" callback="${callback}" onchange="${onchange}"/>
			</td>
			<td>
			</td>
			<td width="100%">
    		    <input type="button" value="Go" onclick="javascript:if (echeck($('${field_id}').value)) window.open('mailto:' + $('${field_id}').value).close();" />
    		</td>
    	</tr>
    </table>
    <span class="fielderror" py:if="error" py:content="error"/>
</span>
