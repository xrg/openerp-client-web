<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="../../templates/master.kid">
<head>
    <title py:content="form.screen.string">Form Title</title>

    <script type="text/javascript">
    
        function do_select(id, src) {
            viewRecord(id, src);
        }

        function toggle_sidebar(forced) {
        
            var sb = MochiKit.DOM.getElement('sidebar');
            var sbp = MochiKit.DOM.getElement('sidebar_pane');

            sb.style.display = forced ? forced : (sb.style.display == "none" ? "" : "none");
            sbp.style.display = sb.style.display;

            set_cookie("terp_sidebar", sb.style.display);

            var img = MochiKit.DOM.getElementsByTagAndClassName('img', null, 'sidebar_hide')[0];
            if (sb.style.display == "none")
                img.src = '/static/images/sidebar_show.gif';
            else
                img.src = '/static/images/sidebar_hide.gif';
        }
        
        MochiKit.DOM.addLoadEvent(function(evt) {
            var sb = MochiKit.DOM.getElement('sidebar');
            if (sb) toggle_sidebar(get_cookie('terp_sidebar'));
                        
            if (!MochiKit.DOM.getElement('_terp_list')) {
                MochiKit.Signal.connect(window.document, 'oncontextmenu', on_context_menu);
            }
        });
        
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
                                        <img src="/static/images/icon.gif"/>
                                    </td>
                                    <td width="100%" py:content="form.screen.string">Form Title</td>
                                    <td nowrap="nowrap" py:if="buttons.search or buttons.form or buttons.calendar or buttons.graph">
                                        <button type="button" title="Search View..." disabled="${tg.selector(not buttons.search)}" onclick="switchView('tree')">Search</button>
                                        <button type="button" title="Form View..." disabled="${tg.selector(not buttons.form)}" onclick="switchView('form')">Form</button>
                                        <button type="button" title="Calendar View..." disabled="${tg.selector(not buttons.calendar)}" onclick="switchView('calendar')">Calendar</button>
                                        <button type="button" title="Graph View..." disabled="${tg.selector(not buttons.graph)}" onclick="switchView('graph')">Graph</button>
                                    </td>
                                    <td align="center" valign="middle" width="16" py:if="buttons.can_attach and not buttons.has_attach">
                                        <img class="button" title="${_('Add an attachment to this resource.')}" src="/static/images/stock/gtk-paste.png" width="16" height="16" onclick="openWindow(getURL('/attachment', {model: '${form.screen.model}', id: ${form.screen.id}}), {name : 'Attachments'})"/>
                                    </td>
                                    <td align="center" valign="middle" width="16" py:if="buttons.can_attach and buttons.has_attach">
                                        <img class="button" title="${_('Add an attachment to this resource.')}" src="/static/images/gtk-paste-v.png" width="16" height="16" onclick="openWindow(getURL('/attachment', {model: '${form.screen.model}', id: ${form.screen.id}}), {name : 'Attachments'})"/>
                                    </td>
                                    <td align="center" valign="middle" width="16" py:if="buttons.i18n">
                                        <img class="button" title="${_('Translate this resource.')}" src="/static/images/translate.png" width="16" height="16" onclick="openWindow('${tg.url('/translator', _terp_model=form.screen.model, _terp_id=form.screen.id)}')"/>
                                    </td>
                                    <td align="center" valign="middle" width="16" py:if="buttons.i18n">
                                        <img class="button" title="${_('View Log.')}" src="/static/images/log.png" width="16" height="16" onclick="openWindow('${tg.url('/viewlog', _terp_model=form.screen.model, _terp_id=form.screen.id)}', {width: 500, height: 300})"/>
                                    </td>
                                    <td align="center" valign="middle" width="16">
                                        <a target="new" href="${tg.query('http://openerp.org/scripts/context_index.php', model=form.screen.model, lang=rpc.session.context.get('lang', 'en'))}"><img class="button" border="0" src="/static/images/stock/gtk-help.png" width="16" height="16"/></a>
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
                                            <button type="button" title="${_('Create a new resource')}" py:if="buttons.new" onclick="editRecord(null)">New</button>
                                            <button type="button" title="${_('Edit this resource')}" py:if="buttons.edit" onclick="editRecord(${form.screen.id or 'null'})">Edit</button>
                                            <button type="button" title="${_('Save this resource')}" py:if="buttons.save" onclick="submit_form('save')">Save</button>
                                            <button type="button" title="${_('Save &amp; Edit this resource')}" py:if="buttons.save" onclick="submit_form('save_and_edit')">Save &amp; Edit</button>
                                            <button type="button" title="${_('Duplicate this resource')}" py:if="buttons.edit" onclick="submit_form('duplicate')">Duplicate</button>
                                            <button type="button" title="${_('Delete this resource')}" py:if="buttons.delete" onclick="submit_form('delete')">Delete</button>
                                            <button type="button" title="${_('Cancel editing the current resource')}" py:if="buttons.cancel" onclick="submit_form('cancel')">Cancel</button>
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
                    <tr>
                        <td class="dimmed-text">
                            [<a onmouseover="showElement('customise_menu_');" onmouseout="hideElement('customise_menu_');" href="javascript: void(0)">Customise</a>]
                            <div id="customise_menu_" class="contextmenu" style="position: absolute; display: none;" onmouseover="showElement(this)" onmouseout="hideElement(this)">
                                <a py:if="links.view_manager"
                                   title="${_('Manage views of the current object')}" 
                                   onclick="openWindow('${tg.url('/viewlist', model=form.screen.model)}', {height: 400})" 
                                   href="javascript: void(0)">Manage Views</a>
                                <a py:if="links.workflow_manager"
                                   title="${_('Manage workflows of the current object')}" 
                                   onclick="openWindow('${tg.url('/workflowlist', model=form.screen.model, active=links.workflow_manager)}', {height: 400})" 
                                   href="javascript: void(0)">Manage Workflows</a>
                                <a py:if="form.screen.model"
                                   title="${_('Customise current object or create a new object')}" 
                                   onclick="openWindow('/viewed/new_model/edit?model=${form.screen.model}')" 
                                   href="javascript: void(0)">Customise Object</a>								   
                            </div>
                        </td>
                    </tr>
                </table>
            </td>

            <td py:if="form.screen.hastoolbar and form.screen.toolbar and form.screen.view_type != 'calendar'" id="sidebar_pane" width="163" valign="top" style="padding-left: 2px">

                <table border="0" cellpadding="0" cellspacing="0" width="160" id="sidebar" style="display:none">
                    <tr py:if="'print' in form.screen.toolbar">
                        <td>
                            <table border="0" cellpadding="0" cellspacing="0" width="100%" class="sidebox">
                                <tr>
                                    <td>
                                        <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                            <tr>
                                                <td width="8" style="background: #ac0000"/>
                                                <td width="7" style="background-color: #363636"/>
                                                <td style="font: verdana; color:white; font-weight:bold; font-size:12px; background-color: #363636">REPORTS</td>
                                                <td width="25" valign="top" style="background: url(/static/images/diagonal_left.gif) no-repeat; background-color: #666666"/>
                                                <td width="50" style="background-color: #666666"/>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>

                                <tr py:for="item in form.screen.toolbar['print']" data="${str(item)}" onclick="submit_form('action', null, getNodeAttribute(this, 'data'))">
                                    <td>
                                        <a href="javascript: void(0)">${item['name']}</a>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    <tr py:if="'action' in form.screen.toolbar">
                        <td>
                            <table border="0" cellpadding="0" cellspacing="0" width="100%" class="sidebox">
                                <tr>
                                    <td>
                                        <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                            <tr>
                                                <td width="8" style="background: #ac0000"/>
                                                <td width="7" style="background-color: #363636"/>
                                                <td style="font: verdana; color:white; font-weight:bold; font-size:12px; background-color: #363636">ACTIONS</td>
                                                <td width="25" valign="top" style="background: url(/static/images/diagonal_left.gif) no-repeat; background-color: #666666"/>
                                                <td width="50" style="background-color: #666666"/>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                                <tr py:for="item in form.screen.toolbar['action']" data="${str(item)}" onclick="submit_form('action', null, getNodeAttribute(this, 'data'))">
                                    <td>
                                        <a href="javascript: void(0)">${item['name']}</a>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    <tr py:if="'relate' in form.screen.toolbar">
                        <td>
                            <table border="0" cellpadding="0" cellspacing="0" width="100%" class="sidebox">
                                <tr>
                                    <td>
                                        <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                            <tr>
                                                <td width="8" style="background: #ac0000"/>
                                                <td width="7" style="background-color: #363636"/>
                                                <td style="font: verdana; color:white; font-weight:bold; font-size:12px; background-color: #363636">LINKS</td>
                                                <td width="25" valign="top" style="background: url(/static/images/diagonal_left.gif) no-repeat; background-color: #666666"/>
                                                <td width="50" style="background-color: #666666"/>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                                <tr py:for="item in form.screen.toolbar['relate']" data="${str(item)}" onclick="submit_form('relate', null, getNodeAttribute(this, 'data'), '${item.get('target', '')}')">
                                    <td>
                                        <a href="javascript: void(0)">${item['name']}</a>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
            </td>

            <td id="sidebar_hide" valign="top" py:if="form.screen.hastoolbar and form.screen.toolbar  and form.screen.view_type != 'calendar'">
               <img src="/static/images/sidebar_show.gif" border="0" onclick="toggle_sidebar();" style="cursor: pointer;"/>
            </td>
        </tr>
    </table>

</body>
</html>
