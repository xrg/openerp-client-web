<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>

<%def name="header()">
    <script type="text/javascript">
        var form_controller = '${path}';
        var USER_ID = '${rpc.session.uid}';
        var RESOURCE_ID = '${rpc.session.active_id}';

        function do_select(id, src) {
            viewRecord(id, src);
        }
        jQuery(document).ready(function() {
            document.title = '${title}' + ' - OpenERP';
            /*
            % if form.screen.view_type == 'form':
            */
            validateForm();
            /*
            % endif
            */
            /*
            % if can_shortcut:
            */
            jQuery('#shortcut_add_remove').click(toggle_shortcut);
            /*
            % endif
            */
            /*
            % if form.screen.model == 'res.request' and form.screen.ids:
            */
            jQuery('ul.tools li a.req_messages small').text('${len(form.screen.ids)}');
            /*
            % endif
            */
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
            <a href="#" onclick="validate_action('${kind}',switchView); return false;"
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
    <table id="main_form_body" class="view" cellpadding="0" cellspacing="0" border="0" width="100%">
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

                    % if form.screen.view_type == 'tree':
                        ${_('Search: %s') % form.screen.string}
                    % else:
                        ${form.screen.string}
                    % endif

                    % if obj_process:
	                    <a class="help" href="${py.url('/view_diagram/process', res_model=form.screen.model, title=form.screen.string, res_id=form.screen.id)}"
	                       title="${_('Corporate Intelligence...')}">
	                        <small>Help</small>
	                    </a>
                    % endif
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
                % if tips:
                    <div id="help-tips">
                        <p>${tips}</p>
                        <a href="/openerp/form/close_or_disable_tips" id="disable-tips" style="text-decoration: underline;">${_("Disable all Tips")}</a>
                        <a href="#hide" id="hide-tips" style="text-decoration: underline;">${_("Hide this Tip")}</a>
                        <br style="clear: both"/>
                    </div>
                % endif
                % if form.screen.view_type == 'form':
                    % if form.logs.logs:
                        ${form.logs.display()}
                    % endif
                % endif
                % if form.screen.view_type in ['form', 'diagram'] and buttons.toolbar and not is_dashboard:
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
                        % if buttons.edit and form.screen.view_type== 'form':
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
                            <label for="show_diagram_grid">${_('Show grid')}:
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
                <div${ " class='non-editable'" if not form.screen.editable and form.screen.view_type == 'form' else "" | n }>${form.display()}</div>

            </td>
            % if form.sidebar:
                <%
                  if form.screen.view_type in ['form', 'calendar', 'gantt']:
                      sidebar_class="open"
                  else:
                      sidebar_class="closed"
                %>
                <td id="main_sidebar" valign="top">
                    <a class="toggle-sidebar ${sidebar_class}" href="#">Toggle</a>
                    <div id="tertiary" class="${sidebar_class}">
                        <div id="tertiary_wrap">
                            ${form.sidebar.display()}
                        </div>
                    </div>
                </td>
                <script type="text/javascript">
                    jQuery('.toggle-sidebar').toggler('#tertiary', function (){
                        jQuery(window).scrollLeft(
                            jQuery(document).width() - jQuery(window).width());
                    });
                </script>
            % endif
        </tr>
    </table>
    <script type="text/javascript">
        jQuery(document).ready(function () {
            var $hide = jQuery('#hide-tips').click(function () {
                jQuery('#help-tips').hide();
                return false;
            });
            jQuery('#disable-tips').click(function () {
                jQuery.post(this.href);
                $hide.click();
                return false;
            })
        })
    </script>
</%def>
