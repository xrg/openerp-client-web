<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="../../templates/master.kid">
<head>
    <title>Manage Workflows ($model)</title>
    <script type="text/javascript">
    
        function do_select(id, src){
            var radio = MochiKit.DOM.getElement(src + '/' + id);
            radio.checked = true;
        }
        
        function doCreate() {
            var vf = getElement('view_form');
            vf.submit();
        }
        
        function doCancel() {
            var edt = getElement('view_editor');
            var lst = getElement('view_list');
            
            edt.style.display = "none";
            lst.style.display = "";
        }
        
        function doClose() {
            window.opener.setTimeout("window.location.reload()", 0);
            window.close();
        }
        
        function onNew() {
            var edt = getElement('view_editor');
            var lst = getElement('view_list');
            
            var nm = getElement('name');
            nm.value = getElement('model').value + '.custom_' + Math.round(Math.random() * 1000);
            
            var osv = getElement('osv')
            osv.value = getElement('model').value
            
            edt.style.display = "";
            lst.style.display = "none";
        }
        
        function onEdit() {
            
            var list = new ListView('_terp_list');
            var boxes = list.getSelectedItems();

            if (boxes.length == 0){
                alert('Please select a workflow...');
                return;
            }
            
            openWindow(getURL('/workflow', {model: getElement('model'), id:boxes[0].value }));
        }
        
        function onRemove() {
        
            var list = new ListView('_terp_list');
            var boxes = list.getSelectedItems();

            if (boxes.length == 0){
                alert('Please select a workflow...');
                return;
            }
            
            if (!window.confirm('Do you really want to remove this workflow?')){
                return;
            }
            
            window.location.href = '/workflowlist/delete?model=${model}&amp;id=' + boxes[0].value;
        }
        
    </script>
</head>
<body>

    <table id="view_list" class="view" cellspacing="5" border="0" width="100%">
        <tr>
            <td>
                <table width="100%" class="titlebar">
                    <tr>
                        <td width="32px" align="center">
                            <img src="/static/images/icon.gif"/>
                        </td>
                        <td width="100%">Manage Workflows ($model)</td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td py:content="screen.display()">List View</td>
        </tr>
        <tr>
            <td>
                <div class="toolbar">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
                        <tr>
                            <td>
                                <button type="button" onclick="onNew()">New</button>
                                <button type="button" onclick="onEdit()">Edit</button>
                                <button type="button" onclick="onRemove()">Remove</button>
                            </td>
                            <td width="100%"></td>
                            <td>
                                <button type="button" onclick="doClose()">Close</button>
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
                            <img src="/static/images/icon.gif"/>
                        </td>
                        <td width="100%">Create a Workflow ($model)</td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td>
                <form id="view_form" action="/workflowlist/create">
                    <input type="hidden" id="model" name="model" value="$model"/>
                    <table width="400" align="center" class="fields">
                        <tr>
                            <td class="label">Workflow Name:</td>
                            <td class="item"><input type="text" id="name" name="name" class="requiredfield"/></td>
                        </tr>
                        <tr>
                            <td class="label">Resource Model:</td>
                            <td class="item"><input type="text" id="osv" name="osv" class="readonlyfield"/></td>
                        </tr>
                        <tr>
                            <td class="label">On Create:</td>
                            <td class="item"><input id="on_create" name="on_create" class="checkbox" type="checkbox" checked=""/></td>                           
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
                                <button type="button" onclick="doCreate()">Save</button>
                                <button type="button" onclick="doCancel()">Cancel</button>
                            </td>
                        </tr>
                    </table>
                </div>
            </td>
        </tr>
    </table>

</body>
</html>
