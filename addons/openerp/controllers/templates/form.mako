<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>

<%def name="header()">
    <title>${form.screen.string}</title>

    <script type="text/javascript">
        var form_controller = '${path}';
        var USER_ID = '${rpc.session.uid}';
    </script>

    <script type="text/javascript">
        function do_select(id, src) {
            viewRecord(id, src);
        }
    </script>
</%def>

<%def name="content()">
	<table id="main_form_body" class="view" cellpadding="0" cellspacing="0" border="0" width="100%" style="border: none;">
        <tr>
            <td id="body_form_td" width="100%" valign="top">
                <table cellpadding="0" cellspacing="0" border="0" width="100%" style="border: none;">
                    % if buttons.toolbar:
                    <tr>
                        <td>
                            <table width="100%" id="title_header">
                                <tr>
                                	% if can_shortcut:
                                		% if rpc.session.active_id not in shortcut_ids:
                                	<td id="add_shortcut" style="padding: 0; width: 30px;">	
	                                    <a href="javascript: void(0)" id="menu_header" 
	                                    	title="${_('Add as shortcut')}" 
	                                    	class="add_shortcut">
	                                    </a>
	                                    <script type="text/javascript">
	                                       jQuery('#menu_header').click(function() {
	                                           jQuery.ajax({
	                                               url: '/openerp/shortcuts/add',
	                                               type: 'POST',
	                                               data: {'id': '${rpc.session.active_id}'},
	                                               success: function() {
	                                                   window.parent.location.reload();
	                                               }
	                                           });
	                                       });
	                                    </script>
	                                </td>
	                                	% endif
                                    % endif
                                    
                                    <td id="title_details" width="30%" class="content_header_space">
                                    	<h1>${form.screen.string}
                                    		<a class="help" href="javascript: void(0)" title="${_('Corporate Intelligence...')}" onclick="show_process_view()">
                                    			<small>Help</small>
		                              		</a>
                                            % if display_name:
		                              		  <small class="sub">${display_name['field']} : ${display_name['value']}</small>
                                            % endif	                              		       
                                    	</h1>
                                    </td>
                                    
                                    %if serverLog:
                                    	<td>
									    	<div id="serverlog" style="display: none;">
									    		<div class="serverLogHeader">
									    			Current actions :
									    			<img id="closeServerLog" style="cursor: pointer;" align="right" src="/openerp/static/images/attachments-a-close.png"></img>
									    		</div>
									    		% for log in serverLog:
									    			<div class="logActions">
								    					<a href="${py.url('/openerp/form/edit', model=log['res_model'], id=log['res_id'])}">
								    						${log['name']}
								    					</a>
									    			</div>
									    		% endfor	
									    	</div>
									    	
									    	<script type="text/javascript">
									    		jQuery('#serverlog').fadeIn('slow');
									    		jQuery('#closeServerLog').click(function() {
									    			jQuery('#serverlog').fadeOut("slow");
									    		});
									    	</script>
								    	</td>
    								% endif
                                    
                                    <%def name="make_view_button(i, kind, name, desc, active)">
                                    	<li class="v${i}" title="${desc}">
                                    		% if form.screen.view_type == kind:
                                    			<a href="javascript: void(0);" onclick="switchView('${kind}')" class="active">${kind}</a>
                                    		% elif kind not in form.screen.view_mode:
                                    		    <a class="nohover">${kind}</a> 
                                    		% else:
                                    			<a href="javascript: void(0);" onclick="switchView('${kind}')">${kind}</a>
                                    		% endif
                                    	</li>
                                    </%def>
                                    
                                    <td id="view_buttons" class="content_header_space">
                                    	<ul class="views-a">
                                    		% for i, view in enumerate(buttons.views):
												${make_view_button(i+1, **view)}
											% endfor
										</ul>
									</td>
									
									<!-- <td class="content_header_space" cursor: pointer;">
	                                    <a onclick="show_process_view()">
		                              		<img title="${_('Corporate Intelligence...')}" class="button" border="0" src="/openerp/static/images/stock/gtk-help.png" width="16" height="16"/>
		                              	</a>
                                    </td> -->
                                  
                                    % if buttons.can_attach and not buttons.has_attach:
                                    <td align="center" valign="middle" width="16" class="content_header_space">
                                        <img 
                                            class="button" width="16" height="16"
                                            title="${_('Show attachments.')}" 
                                            src="/openerp/static/images/stock/gtk-paste.png" 
                                            onclick="window.open(openobject.http.getURL('/openerp/attachment', {model: '${form.screen.model}', id: ${form.screen.id}}))"/>
                                    </td>
                                    % endif
                                    % if buttons.can_attach and buttons.has_attach:
                                    <td align="center" valign="middle" width="16" class="content_header_space">
                                        <img id="attachments"
                                            class="button" width="16" height="16"
                                            title="${_('Show attachments.')}" 
                                            src="/openerp/static/images/stock/gtk-paste-v.png" onclick="window.open(openobject.http.getURL('/openerp/attachment', {model: '${form.screen.model}', id: '${form.screen.id}'}))"/>
                                    </td>
                                    % endif
                                    % if form.screen.view_type in ('form'):
	                                    <td align="center" valign="middle" width="16" class="content_header_space">
	                                        <img 
	                                            class="button" width="16" height="16"
	                                            title="${_('Translate this resource.')}" 
	                                            src="/openerp/static/images/stock/stock_translate.png" onclick="openobject.tools.openWindow(openobject.http.getURL('/openerp/translator', {_terp_model: '${form.screen.model}', _terp_id: ${form.screen.id}, _terp_context: $('_terp_context').value}));"/>
	                                    </td>
	                                    <td align="center" valign="middle" width="16" class="content_header_space">
	                                        <img 
	                                            class="button" width="16" height="16"
	                                            title="${_('View Log.')}" 
	                                            src="/openerp/static/images/stock/stock_log.png"
	                                            onclick="openobject.tools.openWindow('${py.url('/openerp/viewlog', _terp_model=form.screen.model, _terp_id=form.screen.id)}', {width: 500, height: 300})"/>
	                                    </td>
                                    % endif
                                </tr>
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
                            		</td>
                            		<td class="powered">
                            			Powered by <a href="http://www.openerp.com" target="_blank">openerp.com</a>
                            		</td>
                            		<td class="footer" style="text-align: right;">
                            			<a id="show_customize_menu" onmouseover="showCustomizeMenu(this, 'customise_menu_')" 
                                			onmouseout="hideElement('customise_menu_');" href="javascript: void(0)">${_("Customise")}</a><br/>
			                            <div id="customise_menu_" class="contextmenu" onmouseover="showElement(this);" onmouseout="hideElement(this);">
			                                <a class="customise_menu_options" title="${_('Manage views of the current object')}" 
			                                   	onclick="openobject.tools.openWindow('/openerp/viewlist?model=${form.screen.model}', {height: 400})" 
			                                   href="javascript: void(0)">${_("Manage Views")}</a>
			                                <a class="customise_menu_options" title="${_('Manage workflows of the current object')}" 
			                                   	onclick="javascript: show_wkf()" 
			                                   href="javascript: void(0)">${_("Show Workflow")}</a>
			                                <a class="customise_menu_options" title="${_('Customise current object or create a new object')}" 
			                                   	onclick="openobject.tools.openWindow('/openerp/viewed/new_model/edit?model=${form.screen.model}')" 
			                                   href="javascript: void(0)">${_("Customise Object")}</a>
			                            </div>
                            		</td>
                            	</tr>
                            </table>
                        </td>
                    </tr>
                </table>
            </td>

            % if form.sidebar and buttons.toolbar and form.screen.view_type not in ('calendar', 'gantt'):
            <td id="main_sidebar" valign="top">
            	<div id="tertiary">
					<div id="tertiary_wrap">
                		${form.sidebar.display()}
                	</div>
                </div>
            </td>
            % endif
        </tr>
    </table>
</%def>
