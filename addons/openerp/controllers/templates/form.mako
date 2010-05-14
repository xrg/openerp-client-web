<%inherit file="/openerp/controllers/templates/base.mako"/>

<%def name="header()">
    <title>${form.screen.string}</title>

    <script type="text/javascript">
        var form_controller = '${path}';
    </script>

    <script type="text/javascript">
    
        function do_select(id, src) {
            viewRecord(id, src);
        }

    </script>
</%def>

<%def name="content()">
    <%
        if can_shortcut:
            if rpc.session.active_id not in shortcut_ids:
                shortcut_url = py.url('/shortcuts/add', id=rpc.session.active_id)
                shortcut_title = 'Add as shortcut'
                shortcut_picture = '/openerp/static/images/add_shortcut.png'
            else:
                shortcut_url = 'javascript:void(0);'
                shortcut_title = 'Shortcut already added'
                shortcut_picture = '/openerp/static/images/shortcut.png'
    %>
    <table id="main_form_body" class="view" cellpadding="0" cellspacing="0" border="0" width="100%">
        <tr>
            <td width="100%" valign="top">
                <table cellpadding="0" cellspacing="0" border="0" width="100%">
                    % if buttons.toolbar:
                    <tr>
                        <td>
                            <table width="100%" class="titlebar">
                                <tr>
                                	<td>
                                        % if can_shortcut:
                                            <a href="${shortcut_url}" id="menu_header" title="${shortcut_title}">
                                                <img src="${shortcut_picture}" alt="${shortcut_title}" style="padding: 1px;" border="0" width="18px" height="18px"/>
                                            </a>
                                        % endif
	                                </td>
                                    <td width="32px" align="center">
                                        % if form.screen.view_type in ('tree', 'graph'):
                                        <img src="/openerp/static/images/stock/gtk-find.png" alt="Find"/>
                                        % elif form.screen.view_type in ('form'):
                                        <img src="/openerp/static/images/stock/gtk-edit.png" alt="Edit"/>
                                        % elif form.screen.view_type in ('calendar', 'gantt'):
                                        <img src="/openerp/static/images/stock/stock_calendar.png" alt="Calendar"/>
                                        % endif
                                    </td>
                                    <td width="100%">
                                    	${form.screen.string}
                                    	<a target="appFrame" onclick="show_process_view()">
                                    		<img title="${_('Contextual Help..')}" alt="${_('Contextual Help..')}"
                                                 style="height:14px; width:14px;cursor:pointer;" border="0"
                                                 src="/openerp/static/images/iconset-a-help.gif"/>
                                    	</a>
                                    </td>
                                    
                                    <%def name="make_view_button(kind, name, desc, active)">
                                        <button 
                                            type="button" 
                                            title="${desc}" 
                                            onclick="switchView('${kind}')"
                                            ${py.attr_if("disabled", not active)}>${name}</button>
                                    </%def>
                                   
                                    <td nowrap="nowrap">
                                    % for view in buttons.views:
                                        ${make_view_button(**view)}
                                    % endfor                                    
                                    </td>
                                    
                                  
                                    % if buttons.can_attach and not buttons.has_attach:
                                    <td align="center" valign="middle" width="16">
                                        <img alt="${_('Show attachments.')}"
                                            class="button" width="16" height="16"
                                            title="${_('Show attachments.')}" 
                                            src="/openerp/static/images/stock/gtk-paste.png" 
                                            onclick="window.open(openobject.http.getURL('/attachment', {model: '${form.screen.model}', id: ${form.screen.id}}))"/>
                                    </td>
                                    % endif
                                    % if buttons.can_attach and buttons.has_attach:
                                    <td align="center" valign="middle" width="16">
                                        <img alt="${_('Show attachments.')}"
                                            class="button" width="16" height="16"
                                            title="${_('Show attachments.')}" 
                                            src="/openerp/static/images/stock/gtk-paste-v.png" onclick="window.open(openobject.http.getURL('/attachment', {model: '${form.screen.model}', id: '${form.screen.id}'}))"/>
                                    </td>
                                    % endif
                                    % if form.screen.view_type in ('form'):
                                    <td align="center" valign="middle" width="16">
                                        <img alt="${_('Translate this resource.')}"
                                            class="button" width="16" height="16"
                                            title="${_('Translate this resource.')}" 
                                            src="/openerp/static/images/stock/stock_translate.png" onclick="openobject.tools.openWindow('${py.url('/translator', _terp_model=form.screen.model, _terp_id=form.screen.id)}')"/>
                                    </td>
                                    % endif
                                    % if form.screen.view_type in ('form'):
                                    <td align="center" valign="middle" width="16">
                                        <img alt="${_('View Log.')}" 
                                            class="button" width="16" height="16"
                                            title="${_('View Log.')}" 
                                            src="/openerp/static/images/stock/stock_log.png"
                                            onclick="openobject.tools.openWindow('${py.url('/viewlog', _terp_model=form.screen.model, _terp_id=form.screen.id)}', {width: 500, height: 300})"/>
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
                            <div class="toolbar">
                                <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                    <tr>
                                        <td>
                                            % if buttons.new:
                                            <button 
                                                type="button" 
                                                title="${_('Create a new resource')}" 
                                                onclick="editRecord(null)">${_("New")}</button>
                                            % endif
                                            % if buttons.edit:
                                            <button 
                                                type="button" 
                                                title="${_('Edit this resource')}" 
                                                onclick="editRecord(${form.screen.id or 'null'})">${_("Edit")}</button>
                                            % endif
                                            % if buttons.save:
                                            <button 
                                                type="button" 
                                                title="${_('Save this resource')}"
                                                onclick="submit_form('save')">${_("Save")}</button>
                                            <button 
                                                type="button" 
                                                title="${_('Save & Edit this resource')}" 
                                                onclick="submit_form('save_and_edit')">${_("Save & Edit")}</button>
                                            % endif
                                            % if buttons.edit:
                                            <button 
                                                type="button" 
                                                title="${_('Duplicate this resource')}"
                                                onclick="submit_form('duplicate')">${_("Duplicate")}</button>
                                            % endif
                                            % if buttons.delete:
                                            <button 
                                                type="button"
                                                title="${_('Delete this resource')}" 
                                                onclick="submit_form('delete')">${_("Delete")}</button>
                                            % endif
                                            % if buttons.cancel:
                                            <button 
                                                type="button" 
                                                title="${_('Cancel editing the current resource')}" 
                                                onclick="submit_form('cancel')">${_("Cancel")}</button>
                                            % endif
                                        </td>
                                        % if buttons.pager:
                                        <td align="right" nowrap="nowrap" class="pager">${pager.display()}</td>
                                        % endif
                                    </tr>
                                </table>
                            </div>
                        </td>
                    </tr>
                    % endif
                    <tr>
                        <td style="padding: 2px">${form.display()}</td>
                    </tr>
                    
                    <tr>
                        <td class="dimmed-text">
                            [<a onmouseover="showCustomizeMenu(this, 'customise_menu_')" 
                                onmouseout="hideElement('customise_menu_');" href="javascript: void(0)">${_("Customise")}</a>]<br/>
                            <div id="customise_menu_" class="contextmenu" style="position: absolute; display: none;" 
                                 onmouseover="showElement(this);" onmouseout="hideElement(this);">
                                <a title="${_('Manage views of the current object')}" 
                                   onclick="openobject.tools.openWindow('/viewlist?model=${form.screen.model}', {height: 400})" 
                                   href="javascript: void(0)">${_("Manage Views")}</a>
                               <a title="${_('Manage workflows of the current object')}" 
                                   onclick="show_wkf()" 
                                   href="javascript: void(0)">${_("Show Workflow")}</a>
                                <a title="${_('Customise current object or create a new object')}" 
                                   onclick="openobject.tools.openWindow('/viewed/new_model/edit?model=${form.screen.model}')" 
                                   href="javascript: void(0)">${_("Customise Object")}</a>
                            </div>
                        </td>
                    </tr>
                </table>
            </td>

            % if form.sidebar and buttons.toolbar and form.screen.view_type not in ('calendar', 'gantt'):
            <td width="163" valign="top">
                ${form.sidebar.display()}
            </td>
            % endif
        </tr>
    </table>
</%def>
