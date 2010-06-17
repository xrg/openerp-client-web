<form method="post" id="${name}" name="${name}" action="${action}" enctype="multipart/form-data">

    <div>
        <input type="hidden" id="_terp_search_domain" name="_terp_search_domain" value="${search_domain}"/>
        <input type="hidden" id="_terp_filter_domain" name="_terp_filter_domain" value="${filter_domain}"/>
        <input type="hidden" id="_terp_search_data" name="_terp_search_data" value="${search_data}"/>

    % for field in hidden_fields:
        ${display_member(field)}
    % endfor
    </div>

% if screen:
	<table border="0" cellpadding="0" cellspacing="0" width="100%" style="border: none;">
        % if search:
        <tr>
            <td valign="top">${display_member(search)}</td>
        </tr>
        <tr>
            <td class="view_form_options" align="left">
            	<table style="border: none;">
            		<tr>
            			<td style="padding: 0;" width="50%">
            				<div class="toolbar">
			                	<a class="button-a" title="${_('Filter records.')}" href="javascript: void(0)" onclick="search_filter()">${_("Filter")}</a>
			                    
			                    % if screen.editable and (screen.view_type=='tree' and screen.widget.editors):
			                    <a class="button-a" title="${_('Create new record.')}" href="javascript: void(0)" onclick="new ListView('_terp_list').create()">${_("New")}</a>
			                   	% endif
			                   	<a class="button-b" title="${_('Clear all .')}" href="javascript: void(0)">${_("Clear")}</a>
                			</div>
            			</td>
            			<td width="50%" align="left">
            				<div class="message-box" style="width: 100%" width="100%" style="display:none;">
            				</div>
            			</td>
            		</tr>
            	</table>
                
            </td>
            
        </tr>
        % endif
        <tr>
            <td valign="top">${display_member(screen)}</td>
        </tr>
    </table>
% endif
</form>
