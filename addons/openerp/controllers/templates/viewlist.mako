<%inherit file="/openerp/controllers/templates/base.mako"/>

<%def name="header()">
    <title>${_("Manage Views (%s)") % (model)}</title>
    <script type="text/javascript">
    
        function do_select(id, src){
            var radio = openobject.dom.get(src + '/' + id);
			if (radio) {
				radio.checked = true;
			}
        }
        
        function doCreate() {
            var vf = document.forms['view_form'];
            vf.submit();
        }
        
        function doCancel() {
            var edt = openobject.dom.get('view_editor');
            var lst = openobject.dom.get('view_list');
            
            edt.style.display = "none";
            lst.style.display = "";
        }
        
        function doClose() {
            window.close();
        }
        
        function onNew() {
            var edt = openobject.dom.get('view_editor');
            var lst = openobject.dom.get('view_list');
            
            var nm = openobject.dom.get('name');
            nm.value = openobject.dom.get('model').value + '.custom_' + Math.round(Math.random() * 1000);
            
            edt.style.display = "";
            lst.style.display = "none";
        }
        
        function onEdit() {
            
            var list = new ListView('_terp_list');
            var boxes = list.getSelectedItems();

            if (boxes.length == 0){
                alert(_('Please select a view...'));
                return;
            }

            var act = openobject.http.getURL('/openerp/viewed', {view_id: boxes[0].value});
            if (window.opener) {
                window.opener.setTimeout("openobject.tools.openWindow('" + act + "')", 0);
                window.close();
            } else {
                openobject.tools.openWindow(act);
            }
        }
        
        function onRemove() {
        
            var list = new ListView('_terp_list');
            var boxes = list.getSelectedItems();

            if (boxes.length == 0){
                alert(_('Please select a view...'));
                return;
            }
            
            if (!window.confirm(_('Do you really want to remove this view?'))){
                return;
            }
            
            window.location.href = openobject.http.getURL('/openerp/viewlist/delete?model=${model}&id=' + boxes[0].value);
        }
		
        MochiKit.DOM.addLoadEvent(function(evt){
            
            if (!window.opener) 
                return;

            var id = window.opener.document.getElementById('_terp_view_id').value;
            
            if (!openobject.dom.get('_terp_list/' + id)) {
                
                var list = new ListView('_terp_list');
                var ids = list.getRecords();

                if (ids.length) {
                    id = ids[0];
                }
            }
            
            do_select(parseInt(id), '_terp_list');
        });		
        
    </script>
</%def>

<%def name="content()">
    <table id="view_list" class="view" cellspacing="5" border="0" width="100%">
        <tr>
            <td>
                <table width="100%" class="titlebar">
                    <tr>
                        <td width="32px" align="center">
                            <img alt="" src="/openerp/static/images/stock/gtk-find.png"/>
                        </td>
                        <td width="100%">${_("Manage Views (%s)") % (model)}</td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td>${screen.display()}</td>
        </tr>
        <tr>
            <td>
                <div class="toolbar">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
                        <tr>
                            <td>
                            	<a class="button-a" href="javascript: void(0)" onclick="onNew()">${_("New")}</a>
                            </td>
                            <td>
                            	<a class="button-a" href="javascript: void(0)" onclick="onEdit()">${_("Edit")}</a>
                            </td>
                            <td>
                            	<a class="button-a" href="javascript: void(0)" onclick="onRemove()">${_("Remove")}</a>
                            </td>
                            <td width="100%"></td>
                            <td>
                            	<a class="button-a" href="javascript: void(0)" onclick="doClose()">${_("Close")}</a>
                            </td>
                        </tr>
                    </table>
                </div>
            </td>
        </tr>
    </table>
    
    <table id="view_editor" style="display: none;" class="view" cellspacing="5" border="0" width="100%">
        <tr>
            <td>
                <table width="100%" class="titlebar">
                    <tr>
                        <td width="32px" align="center">
                            <img alt="" src="/openerp/static/images/stock/gtk-edit.png"/>
                        </td>
                        <td width="100%">${_("Create a view (%s)") % (model)}</td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td>
                <form id="view_form" action="/openerp/viewlist/create">
                    <input type="hidden" id="model" name="model" value="${model}"/>
                    <table width="400" align="center" class="fields">
                        <tr>
                            <td class="label"><label for="name">${_("View Name:")}</label></td>
                            <td class="item"><input type="text" id="name" name="name" class="requiredfield"/></td>
                        </tr>
                        <tr>
                            <td class="label"><label for="type">${_("View Type:")}</label></td>
                            <td class="item">
                                <select id="type" name="type" class="requiredfield">
                                    <option value="form">Form</option>
                                    <option value="tree">Tree</option>
                                    <option value="graph">Graph</option>
                                    <option value="calendar">Calendar</option>
                                </select>
                            </td>
                        </tr>
                        <tr>
                            <td class="label"><label for="priority">${_("Priority:")}</label></td>
                            <td class="item"><input type="text" id="priority" name="priority"
                                                    value="16" class="requiredfield"/></td>
                        </tr>
                    </table>
                </form>
            </td>
        </tr>
        <tr>
            <td>
                <div class="toolbar">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
                        <tr>
                            <td width="100%"></td>
                            <td>
                            	<a class="button-a" href="javascript: void(0)" onclick="doCreate()">${_("Save")}</a>
                            </td>
                            <td>
                            	<a class="button-a" href="javascript: void(0)" onclick="doCancel()">${_("Cancel")}</a>
                            </td>
                        </tr>
                    </table>
                </div>
            </td>
        </tr>
    </table>
</%def>
