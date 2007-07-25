<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="tinyerp/templates/master.kid">
<head>
    <title py:content="form.screen.string">Form Title</title>
    
    <script type="text/javascript">                 
        function do_select(id, src){
            viewRecord(id, src);            
        }
        
        function toggle_sidebar(element_id, forced) {
            var sb = $(element_id);
            
            sb.style.display = forced ? forced : (sb.style.display == "none" ? "" : "none");            
            set_cookie("terp_sidebar", sb.style.display);

            var img = getElementsByTagAndClassName('img', null, 'sidebar_hide')[0];
            if (sb.style.display == "none")
                img.src = '/static/images/sidebar_show.gif';
            else
                img.src = '/static/images/sidebar_hide.gif';
        }        

        function loadSidebar() {
            var sb = $('sidebar');
            if (sb) toggle_sidebar('sidebar', get_cookie('terp_sidebar'));
        }
        
        connect(window, 'onload', function(){
            registerContextMenu();
            loadSidebar();
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
                                    <td nowrap="nowrap">
                                        <button type="button" title="Search View..." disabled="${tg.selector(not buttons.search)}" onclick="submit_form('switch')">Search</button>
                                        <button type="button" title="Form View..." disabled="${tg.selector(not buttons.form)}" onclick="submit_form('switch')">Form</button>
                                        <button type="button" title="Graph View..." disabled="${tg.selector(not buttons.graph)}" onclick="submit_form('switch')">Graph</button>      
                                        <button type="button" title="Add an attachment to this resource." disabled="${tg.selector(not buttons.attach)}" onclick="openWindow(getURL('/attachment', {model: '${form.screen.model}', id: ${form.screen.id}}), {name : 'Attachments'})">Attachments</button>
                                        <button type="button" title="Launch action about this resource" py:if="buttons.action" onclick="submit_form('action')">Action</button>
                                        <button type="button" title="Print documents" py:if="buttons.report" onclick="submit_form('report')">Print</button>
                                        <button type="button" title="Translate this resource." py:if="buttons.i18n" onclick="openWindow('${tg.url('/translator', _terp_model=form.screen.model, _terp_id=form.screen.id)}')">i18n</button>
                                    </td>
                                    <td align="center" valign="middle" width="16">
                                        <a target="new" href="${tg.query('http://tinyerp.org/scripts/context_index.php', model=form.screen.model, lang=rpc.session.context.get('lang', 'en'))}"><img border="0" src="/static/images/help.png" width="16" height="16"/></a>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
            
                    <tr py:if="len(form.screen.view_mode) > 1 and form.screen.view_mode[0] == 'form'">
                        <td>
            		        <div class="toolbar">
                                <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                    <tr>
                                        <td>
                                            <button type="button" title="Create a new resource" py:if="buttons.new" onclick="submit_form('new')">New</button>
                                            <button type="button" title="Edit this resource" py:if="buttons.edit" onclick="editRecord(${form.screen.id or 'null'})">Edit</button>
                                            <button type="button" title="Save this resource" py:if="buttons.save" onclick="submit_form('save')">Save</button>                                            
                                            <button type="button" title="Delete this resource" py:if="buttons.delete" onclick="submit_form('delete')">Delete</button>
                                            <button type="button" title="Cancel editing the current resource" py:if="buttons.cancel" onclick="viewRecord(${form.screen.id or 'null'})">Cancel</button>
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
                </table>      
            </td>
                       
            <td py:if="form.screen.hastoolbar and form.screen.toolbar" width="163" valign="top" style="padding-left: 2px">
        
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
                                        <a href="#">${item['string']}</a>                                   
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
                                    <td colspan="5">                
                                        <a href="#">${item['string']}</a>                                                           
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
                                <tr py:for="item in form.screen.toolbar['relate']" data="${str(item)}" onclick="submit_form('action', null, getNodeAttribute(this, 'data'))">
                                    <td colspan="5">
                                        <a href="#">${item['string']}</a>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
            </td>
            
            <td id="sidebar_hide" valign="top" py:if="form.screen.hastoolbar and form.screen.toolbar">
               <img src="/static/images/sidebar_show.gif" border="0" onclick="toggle_sidebar('sidebar');" style="cursor: pointer;"/>
            </td>
        </tr>        
    </table> 
    
    <div id="contextmenu" class="contextmenu" onmouseout="hideContextMenu()" onmouseover="showContextMenu()" style="position: absolute; display: none;"/>
    
</body>
</html>
