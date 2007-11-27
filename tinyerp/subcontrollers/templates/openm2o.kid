<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="../../templates/master.kid">
<head>
    <title>${form.screen.string} </title>
    
    <script type="text/javascript">
        var form_controller = '/openm2o';
    </script>

    <script type="text/javascript">       
        function on_load() { 
            if (document.getElementsByName("_terp_id")[0] &amp;&amp; document.getElementsByName("_terp_id")[0].value != 'False')
                window.opener.document.getElementById('${params.source}').value = $("_terp_id").value;
            window.opener.setTimeout("signal($('${params.source}'), 'onchange')", 0);                        
        }
        connect(window, 'onload', on_load);
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
                        <td width="100%" py:content="form.screen.string">Form Title
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
		<tr>
            <td py:content="form.display()">Form View</td>
        </tr>
        <tr>
            <td>
		        <div class="toolbar">
		            <table border="0" cellpadding="0" cellspacing="0" width="100%">
		                <tr>
		                    <td width="100%">
		                    </td>
		                    <td>
		                        <button type="button" onclick="window.close()">Close</button>
		                        <button type="button" onclick="submit_form('save')">Save</button>
		                    </td>
		                </tr>
		            </table>
		        </div>
            </td>
        </tr>
    </table>

</body>
</html>
