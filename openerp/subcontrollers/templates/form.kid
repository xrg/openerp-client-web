<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="../../templates/master.kid">
<head>
    <title py:content="form.screen.string">Form Title</title>

    <script type="text/javascript">
        var form_controller = '$path';
    </script>

    <script type="text/javascript">
    
        function do_select(id, src) {
            viewRecord(id, src);
        }

    </script>

</head>
<body>

    <table class="view" cellpadding="0" cellspacing="0" border="0" width="100%">
        <tr>
            <td width="100%" valign="top">
                <table cellpadding="0" cellspacing="0" border="0" width="100%">
                    <tr>
                        <td>
                            <table width="100%" class="titlebar">
                                <tr>
                                    <td width="32px" align="center">
                                        <img py:if="form.screen.view_type in ('tree', 'graph')" src="/static/images/stock/gtk-find.png"/>
                                        <img py:if="form.screen.view_type in ('form')" src="/static/images/stock/gtk-edit.png"/>
                                        <img py:if="form.screen.view_type in ('calendar', 'gantt')" src="/static/images/stock/stock_calendar.png"/>
                                    </td>
                                    <td width="100%" py:content="form.screen.string">Form Title</td>
                                    <td nowrap="nowrap" py:if="buttons.search or buttons.form or buttons.calendar or buttons.gantt or buttons.graph">
                                        <button 
                                            type="button" 
                                            title="${_('Tree View...')}" 
                                            disabled="${tg.selector(not buttons.search)}" 
                                            onclick="switchView('tree')">Search</button>
                                        <button 
                                            type="button" 
                                            title="${_('Form View...')}" 
                                            disabled="${tg.selector(not buttons.form)}" 
                                            onclick="switchView('form')">Form</button>
                                        <button 
                                            type="button" 
                                            title="${_('Calendar View...')}" 
                                            disabled="${tg.selector(not buttons.calendar)}" 
                                            onclick="switchView('calendar')">Calendar</button>
                                        <button 
                                            type="button" 
                                            title="${_('Gantt View...')}"
                                            disabled="${tg.selector(not buttons.gantt)}" 
                                            onclick="switchView('gantt')">Gantt</button>
                                        <button 
                                            type="button" 
                                            title="${_('Graph View...')}" 
                                            disabled="${tg.selector(not buttons.graph)}" 
                                            onclick="switchView('graph')">Graph</button>
                                        <button 
                                            type="button" 
                                            title="${_('Corporate Intelligence...')}"
                                            onclick="show_process_view()">Process</button>
                                    </td>
                                    <td align="center" valign="middle" width="16" py:if="buttons.can_attach and not buttons.has_attach">
                                        <img 
                                            class="button" width="16" height="16"
                                            title="${_('Add an attachment to this resource.')}" 
                                            src="/static/images/stock/gtk-paste.png" 
                                            onclick="window.open(getURL('/attachment', {model: '${form.screen.model}', id: ${form.screen.id}}))"/>
                                    </td>
                                    <td align="center" valign="middle" width="16" py:if="buttons.can_attach and buttons.has_attach">
                                        <img
                                            class="button" width="16" height="16"
                                            title="${_('Add an attachment to this resource.')}" 
                                            src="/static/images/stock/gtk-paste-v.png" onclick="window.open(getURL('/attachment', {model: '$form.screen.model', id: '$form.screen.id'}))"/>
                                    </td>
                                    <td align="center" valign="middle" width="16" py:if="form.screen.view_type in ('form')">
                                        <img 
                                            class="button" width="16" height="16"
                                            title="${_('Translate this resource.')}" 
                                            src="/static/images/stock/stock_translate.png" onclick="openWindow('${tg.url('/translator', _terp_model=form.screen.model, _terp_id=form.screen.id)}')"/>
                                    </td>
                                    <td align="center" valign="middle" width="16" py:if="form.screen.view_type in ('form')">
                                        <img 
                                            class="button" width="16" height="16"
                                            title="${_('View Log.')}" 
                                            src="/static/images/stock/stock_log.png"
                                            onclick="openWindow('${tg.url('/viewlog', _terp_model=form.screen.model, _terp_id=form.screen.id)}', {width: 500, height: 300})"/>
                                    </td>
                                    <td align="center" valign="middle" width="16">
                                        <a target="_blank" href="${tg.url('http://doc.openerp.com/index.php', model=form.screen.model, lang=rpc.session.context.get('lang', 'en'))}">
                                            <img title="Help links might not work. We will setup the new documentation once we ported all docs to the new documentation system." class="button" border="0" src="/static/images/stock/gtk-help.png" width="16" height="16"/>
                                        </a>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>

                    <tr py:if="form.screen.view_type == 'form' and buttons.toolbar">
                        <td>
                            <div class="toolbar">
                                <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                    <tr>
                                        <td>
                                            <button 
                                                type="button" 
                                                title="${_('Create a new resource')}" 
                                                py:if="buttons.new" 
                                                onclick="editRecord(null)">New</button>
                                            <button 
                                                type="button" 
                                                title="${_('Edit this resource')}" 
                                                py:if="buttons.edit" 
                                                onclick="editRecord(${form.screen.id or 'null'})">Edit</button>
                                            <button 
                                                type="button" 
                                                title="${_('Save this resource')}"
                                                py:if="buttons.save" 
                                                onclick="submit_form('save')">Save</button>
                                            <button 
                                                type="button" 
                                                title="${_('Save &amp; Edit this resource')}" 
                                                py:if="buttons.save" 
                                                onclick="submit_form('save_and_edit')">Save &amp; Edit</button>
                                            <button 
                                                type="button" 
                                                title="${_('Duplicate this resource')}"
                                                py:if="buttons.edit" 
                                                onclick="submit_form('duplicate')">Duplicate</button>
                                            <button 
                                                type="button"
                                                title="${_('Delete this resource')}" 
                                                py:if="buttons.delete"
                                                onclick="submit_form('delete')">Delete</button>
                                            <button 
                                                type="button" 
                                                title="${_('Cancel editing the current resource')}" 
                                                py:if="buttons.cancel" 
                                                onclick="submit_form('cancel')">Cancel</button>
                                        </td>
                                        <td align="right" nowrap="nowrap" py:if="buttons.pager" class="pager" py:content="pager.display()"></td>
                                    </tr>
                                </table>
                            </div>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 2px">${form.display()}</td>
                    </tr>
                    <tr py:if="links">
                        <td class="dimmed-text">
                            [<a onmouseover="MochiKit.Visual.appear('customise_menu_', {from: 0, duration: 0.4});" 
                                onmouseout="hideElement('customise_menu_');" href="javascript: void(0)">Customise</a>]<br/>
                            <div id="customise_menu_" class="contextmenu" style="position: absolute; display: none;" 
                                 onmouseover="showElement(this);" onmouseout="hideElement(this);">
                                <a title="${_('Manage views of the current object')}" 
                                   onclick="openWindow('/viewlist?model=${form.screen.model}', {height: 400})" 
                                   href="javascript: void(0)">Manage Views</a>
                                <a title="${_('Manage workflows of the current object')}" 
                                   onclick="openWindow('/workflowlist?model=${form.screen.model}&amp;active=${links.workflow_manager}', {height: 400})" 
                                   href="javascript: void(0)">Manage Workflows</a>
                                <a title="${_('Customise current object or create a new object')}" 
                                   onclick="openWindow('/viewed/new_model/edit?model=${form.screen.model}')" 
                                   href="javascript: void(0)">Customise Object</a>
                            </div>
                        </td>
                    </tr>
                </table>
            </td>

            <td py:if="form.sidebar and form.screen.view_type not in ('calendar', 'gantt')" width="163" valign="top">
                ${form.sidebar.display()}
            </td>
        </tr>
    </table>

</body>
</html>
