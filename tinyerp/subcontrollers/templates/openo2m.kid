<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="../../templates/master.kid">
<head>
    <title>${form.screen.string} </title>
    
    <script type="text/javascript">
        var form_controller = '/openo2m';
    </script>

    <script type="text/javascript">
    
        function on_load(){
            var pwin = window.opener;
            
            var pform = pwin.document.getElementById('view_form');
            var fields = [];
                        
            forEach(pform.elements, function(e){
                if (e.name &amp;&amp; e.type != 'button' &amp;&amp; e.name.indexOf('${form.screen.prefix}') != 0){
                    var fld = INPUT({'type':'hidden', 'name': e.name, 'id' : e.id, 'onchange' : e.onchange, 'value': e.value});                    
                    fld.disabled = true;
                    
                    fields = fields.concat(fld);
                }
            });
                        
            appendChildNodes('view_form', fields);            
            
            var lc = $('_terp_load_counter').value;
            
            lc = parseInt(lc) || 0;
            
            if (lc > 0) {
                window.opener.setTimeout("new ListView('${form.screen.prefix}').reload()", 0);
            }
            
            if (lc > 1) {
                window.close();
            }
            
        }
        
        connect(window, "onload", on_load);
    </script>

</head>
<body>

    <table class="view" cellspacing="5" border="0" width="100%">
        <tr>
            <td>
                <input type="hidden" id="_terp_load_counter" value="${params.load_counter}"/>
                <table width="100%" class="titlebar">
                    <tr>
                        <td width="32px" align="center">
                            <img src="/static/images/icon.gif"/>
                        </td>
                        <td width="100%" py:content="form.screen.string">Form Title</td>
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
