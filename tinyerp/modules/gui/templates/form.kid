<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="tinyerp/templates/master.kid">
<head>
    <title>${form.screen.string} </title>
    
    <script type="text/javascript" py:if="form.screen.view_mode[0]=='form'">        
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
                            <button onclick="submit_form('edit')">Edit</button>
                            <button>Graph</button>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>

        <tr>
            <td>
		        <div class="toolbar">
		            <table border="0" cellpadding="0" cellspacing="0" width="100%">
		                <tr>
		                    <td width="100%">
		                        <button type="button" title="Create a new resource" onclick="submit_form('new')">New</button>
		                        <button type="button" title="Edit/Save this resource" disabled="${tg.checker(form.screen.view_mode[0] == 'tree')}" onclick="submit_form('save')">Save</button>
		                        <button type="button" title="Delete this resource" disabled="${tg.checker(form.screen.view_mode[0] == 'tree' or not form.screen.id)}" onclick="submit_form('delete')">Delete</button>
		                        <button type="button" title="Go to previois matched search" disabled="${tg.checker(form.screen.view_mode[0] == 'tree')}" onclick="submit_form('prev')">Prev</button>
		                        <button type="button" title="Go to next match search" disabled="${tg.checker(form.screen.view_mode[0] == 'tree')}" onclick="submit_form('next')">Next</button>
		                        <button type="button" title="Find a resource" onclick="submit_form('find')">Find</button>
		                        <button type="button" title="Switch current view: form/list" onclick="submit_form('switch')">Switch</button>
		                    </td>
		                    <td>
		                        <button type="button" title="Launch action about this resource" disabled="${tg.checker(not form.screen.id)}" onclick="submit_form('action')">Action</button>
		                        <button type="button" title="Print documents" disabled="${tg.checker(not form.screen.id)}" onclick="submit_form('report')">Print</button>
		                    </td>
		                </tr>
		            </table>
		        </div>
            </td>
        </tr>
        <tr>
            <td>${form.display()}</td>
        </tr>
    </table>      

</body>
</html>
