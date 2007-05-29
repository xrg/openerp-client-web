<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="tinyerp/templates/master.kid">
<head>
    <title>${form.screen.string} </title>
    
    <script type="text/javascript" py:if="form.screen.view_mode[0]=='form'">
        
        function onCancel() {
        
            var ids = document.getElementsByName('_terp_ids')[0];
            var id = document.getElementsByName('_terp_id')[0];
                        
            ids.value='None'; 
            id.value = 'None';
                        
            submit_form('find');            
        }
        
        function loadSidebar() {
            var sb = $('sidebar');
            if (sb) toggle_sidebar('sidebar', get_cookie('terp_sidebar'));
        }
        
        connect(window, 'onload', loadSidebar);
    </script> 
        
</head>
<body>

    <table class="view" cellspacing="5" border="0" width="100%">
        <tr>
            <td>
                <table width="100%" class="titlebar">
                    <tr>
                        <td width="32px" align="center">
                            <img src="/static/images/icon.gif"/>
                        </td>
                        <td width="100%" py:content="form.screen.string">Form Title</td>
                        <td nowrap="nowrap">
                            <button>Search</button>
                            <button>Edit</button>
                            <button>Graph</button>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>

        <tr>
            <td>
		        <div class="toolbar">
                    <button type="button" title="Create a new resource" onclick="submit_form('new')">New</button>
                    <button type="button" title="Edit current record" py:if="not form.screen.editable" onclick="submit_form('edit')">Edit</button>
                    <button type="button" title="Edit/Save this resource" py:if="form.screen.editable" onclick="submit_form('save')">Save</button>                    
                    <button type="button" title="Delete this resource" py:if="not form.screen.editable" onclick="submit_form('delete')">Delete</button>
                    <button type="button" title="Switch current view: form/list" onclick="submit_form('switch')">Switch</button>
		        </div>
            </td>
        </tr>
        <tr>
            <td>${form.display()}</td>
        </tr>
    </table>      

</body>
</html>
