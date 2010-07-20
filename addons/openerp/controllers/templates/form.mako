<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>

<%def name="header()">
    <%
        if form.screen.view_type == 'form' and display_name:
            title= display_name['field'] + ':' + display_name['value']
        else:
            title = form.screen.string
    %>
    <script type="text/javascript">
        jQuery(document).ready(function() {
            document.title = '${title}' + ' - OpenERP';
        });
    </script>
    <script type="text/javascript">
        var form_controller = '${path}';
        var USER_ID = '${rpc.session.uid}';
        var RESOURCE_ID = '${rpc.session.active_id}';

        function do_select(id, src) {
            viewRecord(id, src);
        }
    </script>
    % if can_shortcut:
    <script type="text/javascript">
        jQuery(document).ready(function () {
            jQuery('#shortcut_add_remove').click(toggle_shortcut);
        });
    </script>
    % endif
</%def>

<%def name="content()">
    <%
        if can_shortcut:
            if rpc.session.active_id in shortcut_ids:
                shortcut_class = "shortcut-remove"
            else:
                shortcut_class = "shortcut-add"

    %>
	<table id="main_form_body" class="view" cellpadding="0" cellspacing="0" border="0" width="100%" style="border: none;">
        <tr>
            <td id="body_form_td" width="100%" valign="top">
                % if buttons.toolbar:
                
                <%def name="make_view_button(i, kind, name, desc, active)">
                    <%
                        cls = ''
                        if form.screen.view_type == kind:
                            cls = 'active'
                    %>
                	<li class="v${i}" title="${desc}">
                		% if kind in form.screen.view_mode:
                			<a href="#" onclick="switchView('${kind}'); return false;"
                			   class="${cls}">${kind}</a>
                		% else:
                		    <a class="inactive">${kind}</a>
                		% endif
                	</li>
                </%def>

            	<ul id="view-selector">
        		% for i, view in enumerate(buttons.views):
					${make_view_button(i+1, **view)}
				% endfor
				</ul>
                % endif
                
            	<h1>
            	    % if can_shortcut:
                    <a id="shortcut_add_remove" href="javascript: void(0)" class="${shortcut_class}"></a>
                    % endif
            	    ${form.screen.string}
            		<a class="help" href="javascript: void(0)"
            		   title="${_('Corporate Intelligence...')}"
            		   onclick="show_process_view('${form.screen.string}')">
            			<small>Help</small>
              		</a>
              		% if serverLog:
              		   <a id="show_server_logs" class="help" href="javascript: void(0)"
                       title="${_('Show Logs...')}">
                            <small>Help</small>
                        </a> 
              		% endif
                    % if display_name:
              		<small class="sub">${display_name['field']} : ${display_name['value']}</small>
                    % endif
            	</h1>
            	
            	%if serverLog:
                <div id="serverlog" style="display: none;">
	                <table class="serverLogHeader">
		                <tr>
                            <td>
                                <img id="closeServerLog" style="cursor: pointer;" align="right" 
                                    src="/openerp/static/images/attachments-a-close.png"></img>
			                </td>
		                </tr>
		                <tr id="actions_row">
			                <td style="padding: 2px 0 0 0;">
				                <table style="width: 100%;">
		                    		% if len(serverLog) > 3:
			                    		% for log in serverLog[-3:]:
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
				                    			<a style="color: blue; font-weight: bold;" href="javascript: void(0);"
				                    			   onclick="jQuery('#more_logs').slideToggle('slow')">
				                    				More...
				                    			</a>
				                    			<div id="more_logs">
				                    			     % for log in serverLog[:-3]:
				                    			         <div>
				                    			             <a href="${py.url('/openerp/form/edit', model=log['res_model'], id=log['res_id'])}">
                                                                ${log['name']}
                                                             </a>
				                    			         </div>
				                    			     % endfor
				                    			</div>
				                    		</td>
				                    	</tr>
				                    	
				                    % else:
				                    	% for log in serverLog:
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
		                </tr>
	                </table>
                </div>

                <script type="text/javascript">
	                jQuery('#serverlog').fadeIn('slow');
	                jQuery('#closeServerLog').click(function() {
		                jQuery('#serverlog').fadeOut("slow");
	                });
	                
	                jQuery('#show_server_logs').click(function() {
	                   jQuery('#serverlog').fadeIn("slow");
	                });
                </script>
                % endif

                % if form.screen.view_type in ['form', 'diagram'] and buttons.toolbar:
                <div class="wrapper">
                	<ul class="inline-b left w50">
					    % if buttons.new:
                        <li title="${_('Create a new resource')}">
                        	<a href="javascript: void(0);" onclick="editRecord(null)" class="button-a">${_("New")}</a>
                        </li>
                    	% endif
                        % if buttons.edit:
                        <li title="${_('Edit this resource')}">
                            <a href="javascript: void(0);" onclick="editRecord(${form.screen.id or 'null'})" class="button-a">${_("Edit")}</a>
                        </li>
                        % endif
                        % if buttons.save:
                        <li title="${_('Save this resource')}">
                            <a href="javascript: void(0);" onclick="submit_form('save')" class="button-a">${_("Save")}</a>
                        </li>
                        <li title="${_('Save & Edit this resource')}">
                            <a href="javascript: void(0);" onclick="submit_form('save_and_edit')" class="button-a">${_("Save & Edit")}</a>
                        </li>
                        % endif
                        % if buttons.edit:
                        <li title="${_('Duplicate this resource')}">
                            <a href="javascript: void(0);" onclick="submit_form('duplicate')" class="button-a">${_("Duplicate")}</a>
                        </li>
                        % endif
                        % if buttons.delete:
                        <li title="${_('Delete this resource')}">
                            <a href="javascript: void(0);" onclick="submit_form('delete')" class="button-a">${_("Delete")}</a>
                        </li>
                        % endif
                        % if buttons.cancel:
                        <li title="${_('Cancel editing the current resource')}">
                            <a href="javascript: void(0);" onclick="submit_form('cancel')" class="button-a">${_("Cancel")}</a>
                        </li>
                        % endif
                	</ul>

                	% if buttons.pager:
                    	<p class="paging-a">
		                	${pager.display()}
					    </p>
                    % endif
                </div>
                % endif
                <div>${form.display()}</div>
                <div class="footer-a">
					<p class="powered">Powered by <a href="http://www.openerp.com/">openerp.com</a></p>
					<p class="one">
						<span>${rpc.session.protocol}://${_("%(user)s", user=rpc.session.loginname)}@${rpc.session.host}:${rpc.session.port}/${rpc.session.db or 'N/A'}</span>
					</p>
				</div>
            </td>
            % if form.sidebar:
            <td class="toggle_sidebar sidebar_close">
            </td>
            <td id="main_sidebar" valign="top">
            	<div id="tertiary" class="sidebar-closed">
					<div id="tertiary_wrap">
                		${form.sidebar.display()}
                	</div>
                </div>
            </td>
            <script type="text/javascript">
                jQuery('td.toggle_sidebar').click(function() {
                    jQuery(this).toggleClass('sidebar_open sidebar_close')
                    toggle_sidebar();
                });
            </script>
            % endif
        </tr>
    </table>
</%def>
