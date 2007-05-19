<form xmlns:py="http://purl.org/kid/ns#" method="post" id="${name}" name="${name}" action="${action}" enctype="multipart/form-data">
    <span py:for="field in hidden_fields" py:replace="field.display(value_for(field), **params_for(field))"/>
    <table border="0" cellpadding="0" cellspacing="0" width="100%" py:if="screen">
        <tr>
            <td py:content="screen.display(value_for(screen), **params_for(screen))"></td>
            <td py:if="screen.hastoolbar and screen.toolbar" width="163" valign="top" style="padding-left: 4px">
                <div id="toolbar_hide">
					<a href="">
						<img src="/static/images/toolbar_hide.png" alt="|" border="0"/>
					</a>
				</div>				
				<table border="0" cellpadding="0" cellspacing="0" width="160">
					<tr>
						<td width="8" bgcolor="#ac0000"></td>
						<td width="7" bgcolor="#363636"></td>
						<td bgcolor="#363636" style="font:verdana; color:white; font-weight:bold; font-size:12px">
							REPORTS
						</td>
						<td width="25" bgcolor="#666666" valign="top">
							<img src="/static/images/head_diagonal.png"/>
						</td>
						<td bgcolor="#666666">
						&nbsp;
						&nbsp;
						&nbsp;
						</td>
					</tr>
					</table>
					<div class="toolbar_button">
					    <span py:for="item in screen.toolbar['print']" data="${str(item)}" onclick="submit_form('action', null, getNodeAttribute(this, 'data'))">
            				<a href="#" class="toolbar_button">${item['string']}</a>
            			</span>
					</div>				
					
					<table border="0" cellpadding="0" cellspacing="0" width="160">
					<tr>
						<td width="8" bgcolor="#ac0000"></td>
						<td width="7" bgcolor="#363636"></td>
						<td bgcolor="#363636" style="font:verdana; color:white; font-weight:bold; font-size:12px">
							ACTIONS
						</td>
						<td width="25" bgcolor="#666666" valign="top">
							<img src="/static/images/head_diagonal.png"/>
						</td>
						<td bgcolor="#666666">
						&nbsp;
						&nbsp;
						&nbsp;
						</td>
					</tr>
				</table>
				<div class="toolbar_button">				    
			        <span py:for="item in screen.toolbar['action']" data="${str(item)}" onclick="submit_form('action', null, getNodeAttribute(this, 'data'))">
       					<a href="#" class="toolbar_button">${item['string']}</a>						
       				</span>
				</div>
	        </td>
        </tr>
    </table>
</form>
