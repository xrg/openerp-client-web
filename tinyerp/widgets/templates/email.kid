<span xmlns:py="http://purl.org/kid/ns#" py:strip="">
	<table width="100%" border="0" cellpadding="0" cellspacing="0">
		<tr>
			<td>
			    <input type="text" kind="${kind}" name='${name}' id ='${field_id}' value="${value}" class="${field_class}" py:attrs="attrs" callback="${callback}" onchange="${onchange}"/>
			</td>
            <td width="2px"><div class="spacer"/></td>
			<td width="75px">
    		    <button type="button" onclick="if (echeck($('${field_id}').value)) window.open('mailto:' + $('${field_id}').value).close();" >
                    Go!
    		    </button>
    		</td>
    	</tr>
    </table>
    <span class="fielderror" py:if="error" py:content="error"/>
</span>
