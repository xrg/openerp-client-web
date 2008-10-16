<table xmlns:py="http://purl.org/kid/ns#" border="0" cellpadding="0" py:if="reports or actions or relates or attachments">
    <tr>
        <td id="sidebar_pane" width="163" valign="top" style="padding-left: 2px">
            <table border="0" cellpadding="0" cellspacing="0" width="160" id="sidebar" style="display:none">
                <tr py:if="reports">
                    <td>
                        <table border="0" cellpadding="0" cellspacing="0" width="100%" class="sidebox">
                            <tr>
                                <td>
                                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                        <tr>
                                            <td width="8" style="background: #ac0000"/>
                                            <td width="7" style="background-color: #363636"/>
                                            <td style="font: verdana; color:white; font-weight:bold; font-size:12px; background-color: #363636">REPORTS</td>
                                            <td width="35" valign="top" style="background: url(/static/images/diagonal_left.gif) no-repeat; background-color: #666666"/>
                                            <td width="50" style="background-color: #666666"/>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
    
                            <tr py:for="item in reports" data="${str(item)}" onclick="submit_form('action', null, getNodeAttribute(this, 'data'))">
                                <td>
                                    <a href="javascript: void(0)">${item['name']}</a>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
                <tr py:if="actions">
                    <td>
                        <table border="0" cellpadding="0" cellspacing="0" width="100%" class="sidebox">
                            <tr>
                                <td>
                                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                        <tr>
                                            <td width="8" style="background: #ac0000"/>
                                            <td width="7" style="background-color: #363636"/>
                                            <td style="font: verdana; color:white; font-weight:bold; font-size:12px; background-color: #363636">ACTIONS</td>
                                            <td width="35" valign="top" style="background: url(/static/images/diagonal_left.gif) no-repeat; background-color: #666666"/>
                                            <td width="50" style="background-color: #666666"/>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                            <tr py:for="item in actions" data="${str(item)}" onclick="submit_form('action', null, getNodeAttribute(this, 'data'))">
                                <td>
                                    <a href="javascript: void(0)">${item['name']}</a>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
                <tr py:if="relates">
                    <td>
                        <table border="0" cellpadding="0" cellspacing="0" width="100%" class="sidebox">
                            <tr>
                                <td>
                                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                        <tr>
                                            <td width="8" style="background: #ac0000"/>
                                            <td width="7" style="background-color: #363636"/>
                                            <td style="font: verdana; color:white; font-weight:bold; font-size:12px; background-color: #363636">LINKS</td>
                                            <td width="35" valign="top" style="background: url(/static/images/diagonal_left.gif) no-repeat; background-color: #666666"/>
                                            <td width="50" style="background-color: #666666"/>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                            <tr py:for="item in relates" data="${str(item)}" onclick="submit_form('relate', null, getNodeAttribute(this, 'data'), '${item.get('target', '')}')">
                                <td>
                                    <a href="javascript: void(0)">${item['name']}</a>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
                
                <tr py:if="attachments">
                    <td>
                        <table border="0" cellpadding="0" cellspacing="0" width="100%" class="sidebox">
                            <tr>
                                <td>
                                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                        <tr>
                                            <td width="8" style="background: #ac0000"/>
                                            <td width="7" style="background-color: #363636"/>
                                            <td style="font: verdana; color:white; font-weight:bold; font-size:12px; background-color: #363636">ATTACHMENTS</td>
                                            <td width="35" valign="top" style="background: url(/static/images/diagonal_left.gif) no-repeat; background-color: #666666"/>
                                            <td width="50" style="background-color: #666666"/>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                            <tr py:for="item in attachments" data="${str(item)}">
                                <td>
                                    <a href="/attachment/save_as/${item[1]}?record=${item[0]}">${item[1]}</a>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
                
            </table>
        </td>

        <td id="sidebar_hide" valign="top">
           <img src="/static/images/sidebar_show.gif" border="0" onclick="toggle_sidebar();" style="cursor: pointer;"/>
        </td>
    </tr>
</table>
