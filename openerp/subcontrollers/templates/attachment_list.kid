<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="../../templates/master.kid">
<head>
    <title>Attachments</title>
    <script type="text/javascript" src="/static/javascript/attachment.js"></script>
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
                        <td width="100%">Attachments List</td>
                    </tr>
                </table>
            </td>
        </tr>
        
        <tr>
            <td py:content="screen.display()">List View</td>
        </tr>
        <tr>
            <td>
            	<form action="/attachment" method="post" enctype="multipart/form-data">
            		<input type="hidden" name="model" value="${model}"/>
                	<input type="hidden" name="id" value="${id}"/>
	                <div class="toolbar">
	                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
	                        <tr>
	                            <td align="left">
	                                <button type="button" onclick="do_add(form)">Add</button>
	                            </td>
	                            <td align="left">
	                                <button type="button" onclick="do_edit(form)">Edit</button>
	                            </td>
	                            <td align="left">
	                                <button type="button" onclick="do_delete(form)">Delete</button>
	                            </td>
	                            <td>
	                            	<button type="button" onclick="do_save(form)">Save As</button>
	                           	</td>
	                            <td width="100%" align="right">
	                                <button type="button" onclick="window.close()">Close</button>
	                            </td>
	                        </tr>
	                    </table>
	                </div>
                </form>
            </td>
        </tr>
    </table>

</body>
</html>
