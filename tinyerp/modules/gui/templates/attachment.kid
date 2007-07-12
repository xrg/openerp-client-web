<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="tinyerp/templates/master.kid">
<head>
    <title>Attachments</title>
    <script type="text/javascript">
    
        function do_select(id, src){
        }
        
        function do_upload(form){
            form.action = '/attachment/add';
            form.submit();
        }
        
        function do_save(form){

            var list = new ListView('_terp_list');
            var boxes = list.getSelected();
            
            if (boxes.length == 0){
                alert('Please select a resouce...');
                return;                
            }
            
            var id = boxes[0].value;
            
            var p = boxes[0].parentNode.parentNode;
            var a = getElementsByTagAndClassName('a', null, p)[0];
            
            var fname = '/' + a.innerHTML;
            
            form.action = getURL('/attachment/save' + fname, {record: id});
            form.submit();           
        }

        function do_delete(form){
            var list = new ListView('_terp_list');
            var boxes = list.getSelected();
            
            if (boxes.length == 0){
                alert('Please select a resouce...');
                return;                
            }
            
            var id = boxes[0].value;
            
            form.action = getURL('/attachment/delete', {record: id});
            form.submit();
        }

        function check_for_popup() {
            if(window.opener) {
                var h = $('header');
                var f = $('footer');
                h.parentNode.removeChild(h);
                f.parentNode.removeChild(f);
                var s = $('sidebar_hide');
                if(s)
                    s.parentNode.removeChild(s);
            }                        
        }       
        connect(window, 'onload', check_for_popup);
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
                        <td width="100%">Attachments</td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td>
                <div class="toolbar">
                    <form action="/attachment/add" method="post" enctype="multipart/form-data">
                        <input type="hidden" name="model" value="${model}"/>
                        <input type="hidden" name="id" value="${id}"/>
                        <table border="0" cellpadding="0" cellspacing="0" width="100%">
                            <tr>
                                <td class="label">Add Rresource: </td>
                                <td><input type="file" id="uploadfile" name="uploadfile" onchange="do_upload(form)"/></td>
                                <td width="100%"></td>
                                <td><button type="button" onclick="do_save(form)">Save As</button></td>
                                <td><button type="button" onclick="do_delete(form)">Delete</button></td>                            
                            </tr>
                        </table>
                    </form>
                </div>
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
		                    <td width="100%">
		                    </td>
		                    <td>
		                        <button type="button" onclick="window.close()">Close</button>
		                    </td>
		                </tr>
		            </table>
		        </div>
            </td>
        </tr>
    </table>

</body>
</html>
