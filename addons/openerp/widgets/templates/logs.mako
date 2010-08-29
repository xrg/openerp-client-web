% if logs:
<div id="serverlog">
    <table class="serverLogHeader">
        <tr id="actions_row">
            <td style="padding: 2px 0 0 0;">
                <table style="width: 100%;">
                    % if len(logs) > 3:
                        % for log in logs[-3:]:
                            <tr>
                                <td class="logActions">
                                    <a href="${py.url('/openerp/form/edit', model=log['res_model'], id=log['res_id'])}">
                                        ${log['name']}
                                    </a>
                                </td>
                            </tr>
                        % endfor
                        <tr>
                            <td style="padding: 0 0 0 10px;">
                                <a id="more" style="color: blue; font-weight: bold;" href="javascript: void(0);"
                                   onclick="jQuery(this).hide();
                                   			jQuery('#more_logs').slideDown('slow');
                                   			jQuery('#less').show();">
                                    ${_('More...')}
                                </a>
                                <div id="more_logs">
                                     % for log in logs[:-3]:
                                         <div>
                                             <a href="${py.url('/openerp/form/edit', model=log['res_model'], id=log['res_id'])}">
                                                ${log['name']}
                                             </a>
                                         </div>
                                     % endfor
                                     <a id="less" style="color: blue; font-weight: bold;" href="javascript: void(0);"
                                   onclick="jQuery(this).hide();
                                   			jQuery('#more_logs').slideUp('slow');
                                   			jQuery('#more').show();">
                                    ${_('Less...')}
                                	</a>
                                </div>
                            </td>
                        </tr>
                        
                    % else:
                        % for log in logs:
                            <tr>
                                <td class="logActions">
                                    <a href="${py.url('/openerp/form/edit', model=log['res_model'], id=log['res_id'])}">
                                        ${log['name']}
                                    </a>
                                </td>
                            </tr>
                        % endfor
                    % endif
                </table>
            </td>
            <td style="padding: 0;" valign="top">
                <img id="closeServerLog" style="cursor: pointer;" align="right" 
                    src="/openerp/static/images/attachments-a-close.png"></img>
            </td>
        </tr>
    </table>
</div>

<script type="text/javascript">
    jQuery('#serverlog').show();
    jQuery('#closeServerLog').click(function() {
        jQuery('#serverlog').hide();
    });
    
    jQuery('#show_server_logs').click(function() {
       jQuery('#serverlog').show();
    });
</script>
% endif