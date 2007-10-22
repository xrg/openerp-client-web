<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="tinyerp/templates/master.kid">
<head>
    <title>${form.screen.string}</title>
    
    <script type="text/javascript">
        var form_controller = '/calpopup';
    </script>

    <script type="text/javascript">
    
        function load_defaults() {        
            var pwin = window.opener;
            var elem = pwin.document.getElementById('calEventNew');
            
            var starts = getNodeAttribute(elem, 'dtStart');
            var ends = getNodeAttribute(elem, 'dtEnd');
            
            var params = {
		        '_terp_model': $('_terp_model').value,
		        '_terp_fields': pwin.document.getElementById('_terp_calendar_fields').value,
		        '_terp_starts' : starts,
		        '_terp_ends' : ends,
		        '_terp_context': $('_terp_context').value
		    }
            
            var req = Ajax.JSON.post('/calpopup/get_defaults', params);
            req.addCallback(function(obj){
                forEach(items(obj), function(item){
                    var k = item[0];
                    var v = item[1];
                    
                    var e = getElement(k);
                    
                    if (e) e.value = v;
                });
            });        
        }
    
        function on_load() {
            var id = $('_terp_id').value || false;
            
            if (!id || id == 'False') {
                load_defaults();
            }
        }
        
        window.onbeforeunload = function(){
            var id = $('_terp_id').value || false;
            
            if (id &amp;&amp; id != 'False') {
                window.opener.setTimeout('getCalendar()', 0);
            }            
        }
        
        addLoadEvent(on_load);
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
