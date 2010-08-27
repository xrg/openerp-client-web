	<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>

<%def name="header()">
	<script type="text/javascript">
        jQuery(document).ready(function() {
            document.title = '${title}' + ' - OpenERP';
            adjustTopWidth();
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
                        <a id="shortcut_add_remove" title="${_('Add / Remove Shortcut...')}" href="javascript: void(0)" class="${shortcut_class}"></a>
                    % endif
                    ${form.screen.string}
                    <a class="help" href="javascript: void(0)"
                       title="${_('Corporate Intelligence...')}"
                       onclick="show_process_view('${form.screen.string}')">
                        <small>Help</small>
                      </a>
                      % if form.screen.view_type == 'form' and form.logs.logs:
                         <a id="show_server_logs" class="help" href="javascript: void(0)"
                       title="${_('Show Logs...')}">
                            <small>Help</small>
                        </a>
                      % endif
                    % if display_name:
                          <small class="sub">${display_name['field']} : ${display_name['value']}</small>
                    % endif
                </h1>
				% if form.screen.view_type == 'form':
					% if form.logs.logs:
						${form.logs.display()}
					% endif
				% endif
                % if form.screen.view_type in ['form', 'diagram'] and buttons.toolbar and form.screen.model != 'board.board':
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

	                    var total_win_width = jQuery('#main_form_body').width();
	                    jQuery(window).scrollLeft(total_win_width);
	                });
	            </script>
            % endif
        </tr>
    </table>
</%def>
