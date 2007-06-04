<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="tinyerp/templates/master.kid">
<head>
    <title py:content="form.screen.string">Form Title</title>
    
    <script type="text/javascript">                 
        function do_select(id){
            form = $('view_form');
            form.action = '/form/view';
            form._terp_id.value = id;
            
            form.submit();
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
        
        connect(window, 'onload', loadSidebar);
    </script> 
        
</head>
<body>

    <table class="view" cellpadding="0" cellspacing="0" border="0" width="100%">
        <tr>
            <td width="100%">
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
                                            <button type="button" title="Edit current record" py:if="buttons.edit" onclick="submit_form('edit')">Edit</button>
                                            <button type="button" title="Edit/Save this resource" py:if="buttons.save" onclick="submit_form('save')">Save</button>
                                            <button type="button" title="Cancel editing the current resource" py:if="buttons.cancel" onclick="submit_form('cancel')">Cancel</button>
                                            <button type="button" title="Delete this resource" py:if="buttons.delete" onclick="submit_form('delete')">Delete</button>
                                        </td>
                                        <td align="right" nowrap="nowrap" py:if="buttons.pager" class="pager">
                                            
                                            <span py:if="(form.screen.offset&lt;0) or (form.screen.offset is 0)" class="disabled_text">
											    <img border="0" align="absmiddle" src="/static/images/pager_start_off.gif"/> Start
											</span>
											<span py:if="(form.screen.offset&gt;0)">
											    <a href="javascript: void(0)" onclick="submit_form('first'); return false;">
											        <img border="0" align="absmiddle" src="/static/images/pager_start.gif"/> <b>Start</b>
											    </a>
											</span>   				                               
                                           
                                            <span py:if="(form.screen.offset&lt;0) or (form.screen.offset is 0)" class="disabled_text">
											    <img border="0" align="absmiddle" src="/static/images/pager_prev_off.gif"/> Previous
											</span>
											<span py:if="(form.screen.offset&gt;0)">
											    <a href="javascript: void(0)" onclick="submit_form('previous'); return false;">
											        <img border="0" align="absmiddle" src="/static/images/pager_prev.gif"/> <b>Previous</b>
											    </a>
					                        </span>

                                            <a href="javascript: void(0)">(1st of ${form.screen.offset} to ${form.screen.limit + form.screen.offset})</a>

                                            <span py:if="not form.screen.ids" class="disabled_text">
					                            Next <img border="0" align="absmiddle" src="/static/images/pager_next_off.gif"/>
											</span>
					                        <span py:if="form.screen.ids">
					       						<a href="javascript: void(0)" onclick="submit_form('next'); return false;">
					       						    <b>Next </b><img border="0" align="absmiddle" src="/static/images/pager_next.gif"/>
					       						</a>
					                        </span>
					                                                                                    
                                            <span py:if="not form.screen.ids" class="disabled_text">
					                            End <img border="0" align="absmiddle" src="/static/images/pager_end_off.gif"/>
											</span>						
											<span py:if="form.screen.ids">
					    						<a href="javascript: void(0)" onclick="submit_form('last'); return false;">
					    						    <b>End </b><img border="0" align="absmiddle" src="/static/images/pager_end.gif"/>
					    						</a>
					    				    </span>
                                            
                                        </td>
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
                                                <td width="25" valign="top" style="background: url(/static/images/head_diagonal.png) no-repeat; background-color: #666666"/>
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
                                                <td width="25" valign="top" style="background: url(/static/images/head_diagonal.png) no-repeat; background-color: #666666"/>
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
                </table>              
            </td>               
            
            <td id="sidebar_hide" valign="top" py:if="form.screen.hastoolbar and form.screen.toolbar">
               <img src="/static/images/sidebar_show.gif" border="0" onclick="toggle_sidebar('sidebar');" style="cursor: pointer;"/>
            </td>            
            
        </tr>
    </table>
</body>
</html>
