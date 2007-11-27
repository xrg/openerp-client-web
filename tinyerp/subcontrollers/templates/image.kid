<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="../../templates/master.kid">
<head>
    <title>Image</title>
    <script type="text/javascript">

    	function do_delete(form, id, field){
            form.attributes['action'].value = getURL('/image/delete', {id: id});
            form.submit();
        }

        function do_save(form, id){
            form.attributes['action'].value = getURL('/image/save_as', {id: id});
            form.submit();
        }

		addLoadEvent(function(evt){
			img = window.opener.document.getElementById('${field}');
			img.src = img.src + '&amp;' + Math.random();
        });

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
                        <td width="100%">Image</td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td>
                <form action="/image/add" method="post" enctype="multipart/form-data">
	                    <input type="hidden" name="model" value="${model}"/>
	                    <input type="hidden" name="id" value="${id}"/>
	                    <input type="hidden" name="field" value="${field}"/>
                        <div class="toolbar">
	                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
	                        <tr>
	                            <td class="label">Add Resource: </td>
	                            <td width="100%"><input type="file" id="upimage" name="upimage"/></td>
	                        </tr>
	                    </table>
					</div>
					<div class="spacer"></div>
	                <div class="toolbar">
	                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
	    					<tr>
	    						<td width="100%">
	    						<button type="submit">Save</button>
	    						<button type="button" onclick="do_save(form, id)">Save As</button>
								<button type="button" onclick="do_delete(form, id, field)">Delete</button>
		                    	</td>
			        	        <td>
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