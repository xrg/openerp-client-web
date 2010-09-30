<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>

<%def name="header()">
	<script type="text/javascript">
        jQuery(document).ready(function() {
            document.title = '${title}' + ' - OpenERP';
        });
    </script>
    % if form.screen.view_type == 'form':
        <script type="text/javascript">
            jQuery(document).ready(function() {
                validateForm();
            });
        </script>
    % endif
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
	
	% if form.screen.model == 'res.request' and form.screen.ids:
		<script type="text/javascript">
			jQuery(document).ready(function () {
				jQuery('ul.tools li a.req_messages small').text('${len(form.screen.ids)}')
			});
		</script>
	% endif

	<script type="text/javascript">
        jQuery('#helpTips').show();
        jQuery('#closeHelpTips').click(function() {
            jQuery('div#helpTips').hide();
        });
        jQuery('#closeHelpTips_all').click(function() {
            jQuery('div#helpTips').hide();
            openobject.http.postJSON('/openerp/form/close_or_disable_tips');
        });
    </script>

</%def>

<%def name="make_view_button(kind, name, desc)">
    <%
        cls = ''
        if form.screen.view_type == kind:
            cls = 'active'
    %>
    <li class="${kind}" title="${desc}">
        % if kind in form.screen.view_mode:
            <a href="#" onclick="switchView('${kind}'); return false;"
               class="${cls}">${kind}</a>
        % else:
            <a href="#" class="inactive">${kind}</a>
        % endif
    </li>
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
                    <ul id="view-selector">
                    % for view in buttons.views:
                        ${make_view_button(**view)}
                    % endfor
                    </ul>
                % endif

                <h1>
                    % if can_shortcut:
                        <a id="shortcut_add_remove" title="${_('Add / Remove Shortcut...')}" href="javascript: void(0)" class="${shortcut_class}"></a>
                    % endif
                    ${form.screen.string}
                    <a class="help" href="javascript: void(0)"
                       title="${_('Corporate Intelligence...')}"
                       onclick="show_process_view('${form.screen.string}')">
                        <small>Help</small>
                      </a>
                      % if form.screen.view_type == 'form' and form.logs.logs:
                         <a id="show_server_logs" class="logs" href="javascript: void(0)"
                       title="${_('Show Logs...')}">
                            <small>Logs</small>
                        </a>
                      % endif
                    % if display_name:
                          <small class="sub">${display_name['field']} : ${display_name['value']}</small>
                    % endif
                </h1>
                % if can_shortcut and tips and show_menu_help:
                    <div id="helpTips">
                        <table width="100%" style="border:none">
                            <tr id="tips_row">
                                <td>
                                    <h3 style="padding-left:5px; color: #511712;">${title} - ${_("Tips")}</h3>
                                </td>
                                <td valign="top" style="padding:1px 1px 0 0;" align="right">
                                    <button id="closeHelpTips" type="button" style="padding:0">${_("Close Tip")}</button>
                                    <button id="closeHelpTips_all" type="button" style="padding:0">${_("Disable all Tips")}</button>
                                </td>
                            </tr>
                            <tr>
                                <td colspan="2" style="padding:3px 5px;">${tips}</td>
                            </tr>
                        </table>
                    </div>
                % endif
				% if form.screen.view_type == 'form':
					% if form.logs.logs:
						${form.logs.display()}
					% endif
				% endif
                % if form.screen.view_type in ['form', 'diagram'] and buttons.toolbar and form.screen.model != 'board.board':
                <div class="wrapper action-buttons">
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
                        % if buttons.create_node:
                        <li title="${_('Create new node')}">
                            <a href="javascript: void(0);" onclick="create_node()" class="button-a">${_("New Node")}</a>
                        </li>
                        % endif
                        % if buttons.show_grid:
                        <li title="${_('Show grid in workflow canvas')}">
                            <label for="show_diagram_grid">Show grid:
                                <input type="checkbox" checked="checked" class="checkbox" id="show_diagram_grid"
                                       value="" onchange="show_grid(this); return false">
                            </label>
                        </li>
                        % endif
                    </ul>

                    % if buttons.pager:
                        ${pager.display()}
                    % endif
                </div>
                % endif
                <div>${form.display()}</div>

            </td>
            % if form.sidebar:
	            <td class="toggle_sidebar sidebar_close"></td>
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
                        jQuery(window).trigger('on-appcontent-resize');

                        // Scroll to see right sidebar
                        jQuery(window).scrollLeft(
                            jQuery(document).width() - jQuery(window).width());
                    });
	            </script>
            % endif
        </tr>
    </table>
</%def>
