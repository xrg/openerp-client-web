<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>

<%def name="header()">
    <title>${form.screen.string}</title>

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
                <table cellpadding="0" cellspacing="0" border="0" width="100%" style="border: none;">
                    % if buttons.toolbar:
                    <tr>
                        <td style="padding: 10px 10px 5px 0;">
                            <table width="100%" id="title_header">
                                <tr>
                                	% if can_shortcut:
                                        <td id="shortcut_add_remove" class="${shortcut_class}"></td>
                                    % endif

                                    <td id="title_details" width="30%" class="content_header_space">
                                    	<h1>${form.screen.string}
                                    		<a class="help" href="javascript: void(0)" title="${_('Corporate Intelligence...')}" onclick="show_process_view('${form.screen.string}')">
                                    			<small>Help</small>
		                              		</a>
                                            % if display_name:
		                              		  <small class="sub">${display_name['field']} : ${display_name['value']}</small>
                                            % endif
                                    	</h1>
                                    </td>

                                    <%def name="make_view_button(i, kind, name, desc, active)">
                                        <%
                                            cls = ''
                                            if form.screen.view_type == kind:
                                                cls = 'active'
                                        %>
                                    	<li class="v${i}" title="${desc}">
                                    		% if kind in form.screen.view_mode:
                                    			<a href="#" onclick="switchView('${kind}'); return false;" class="${cls}">${kind}</a>
                                    		% else:
                                    		    <a class="inactive">${kind}</a>
                                    		% endif
                                    	</li>
                                    </%def>

                                    <td id="view_buttons" class="content_header_space">
                                    	<ul id="view-selector">
                                    		% for i, view in enumerate(buttons.views):
												${make_view_button(i+1, **view)}
											% endfor
										</ul>
									</td>                                    
                                </tr>
                                %if serverLog:
	                            	<tr>
		                              	<td colspan="4" style="width: 100%; padding: 0px;">
									    	<div id="serverlog" style="display: none;">
									    		<table class="serverLogHeader">
									    			<tr>
									    				<td style="padding: 2px 10px 0 10px; font-weight: bold;">
									    					<img id="toggle_server_log" style="cursor: pointer; padding-bottom: 3px;" src="/openerp/static/images/server_log_close.gif"></img>
											    			Current actions :
											    			<td>
											    				<img id="closeServerLog" style="cursor: pointer;" align="right" src="/openerp/static/images/attachments-a-close.png"></img>
											    			</td>
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
															    		<td style="font-weight: bold; padding: 0 0 0 10px;">
															    			<a style="color: blue;" href="javascript: void();" onclick="openobject.tools.openWindow('${py.url('/openerp/form')}', {width: 550, height: 340});">
															    				More...
															    			</a>
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
									    		
									    		jQuery('img#toggle_server_log').click(function() {
									    			var server_img_src = jQuery(this).attr('src');
									    			if (jQuery(this).attr('src').indexOf('server_log_close') > 0) {
									    				jQuery('tr#actions_row').css('display', 'none');
									    				jQuery(this).attr('src', server_img_src.replace('server_log_close', 'server_log_open'));
									    				jQuery(this).css('padding-bottom', '1px');
									    			}
									    			else {
									    				jQuery('tr#actions_row').css('display', '');
									    				jQuery(this).css('padding-bottom', '3px');
									    				jQuery(this).attr('src', server_img_src.replace('server_log_open', 'server_log_close'));
									    			}
									    		});
									    	</script>
								    	</td>
								    </tr>
								% endif
                            </table>
                        </td>
                    </tr>
                    % endif

                    % if form.screen.view_type in ['form', 'diagram'] and buttons.toolbar:
                    <tr>
                        <td>
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
                        </td>
                    </tr>
                    % endif
                    <tr>
                        <td style="padding: 2px">${form.display()}</td>
                    </tr>
                    <tr>
                        <td class="dimmed-text">
                            <table class="form-footer">
                            	<tr>
                            		<td class="footer">
                            			<a href="javascript: void(0)" onclick="new ListView('_terp_list').importData()"">${_("Import")}</a>
                            			<span>|</span>
                            			<a href="javascript: void(0)" onclick="new ListView('_terp_list').exportData()">${_("Export")}</a>
                            			% if form.screen.view_type in ('form'):
	                           			 <span>|</span>
		                           			 <a href="javascript: void(0)" title="${_('Translate this resource.')}" onclick="openobject.tools.openWindow(openobject.http.getURL('/openerp/translator', {_terp_model: '${form.screen.model}', _terp_id: ${form.screen.id}, _terp_context: $('_terp_context').value}));">
		                           			      ${_('Translate')}</a>
		                           			 <span>|</span>
		                           			 <a href="javascript: void(0)"  title="${_('View Log.')}" onclick="openobject.tools.openWindow('${py.url('/openerp/viewlog', _terp_model=form.screen.model, _terp_id=form.screen.id)}', {width: 550, height: 340});">
		                           			     ${_('View Log')}
		                           			 </a> 
                            			% endif
                            		</td>                            		
                            		<td class="powered">
                            			Powered by <a href="http://www.openerp.com" target="_blank">openerp.com</a>
                            		</td>
                            	</tr>
                            </table>
                        </td>
                    </tr>
                </table>
            </td>

            % if form.sidebar:
            <td id="main_sidebar" valign="top">
            	<div id="tertiary" class="sidebar-closed">
					<div id="tertiary_wrap">
                		${form.sidebar.display()}
                	</div>
                </div>
            </td>
            % endif
        </tr>
    </table>
</%def>
