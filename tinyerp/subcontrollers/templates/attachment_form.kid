<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="../../templates/master.kid">
<head>
    <title>Attachments</title>
    
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
                        <td width="100%">Attachments Form</td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td>
                <form action="/attachment/save" method="post" enctype="multipart/form-data">
                    <input type="hidden" name="model" value="${model}"/>
                    <input type="hidden" name="id" value="${id}"/>
                    <input type="hidden" name="record" value="${record}"/>
                    <div class="toolbar">
                        <table border="0" cellpadding="0" cellspacing="0" width="100%">
                            <tr>
                                <td class="label" align="left">Add Resource : </td>
                                <td py:if="fname" width="100%">
                                	<input type="file" id="uploadfile" name="uploadfile"> ${fname} </input>
                                </td>
                                <td py:if="not fname" width="100%"><input type="file" id="uploadfile" name="uploadfile"/></td>                                                                
                            </tr>
                        </table>
                    </div>
                    <table width="100%">
                    	<tr>
                    		<td class="item" align="left">
                    			Description :
                    			<textarea name="description" rows="6">${desc}</textarea>
                    		</td>           		
	                   	</tr>
	                </table>
	                <hr/>
					<table width="100%">
                    	<tr>
                    		<td class="item" align="center" width="70%" height="250px">
                    			<table border='0' width="100%" height="100%">
                    				<tr>
                    					<td width="100%" height="100%" align="center" py:if="ext">
                    					 	<img src="/attachment/get_image?record=${record}"/>
                    					</td>
                    					<td width="100%" height="100%" align="center" py:if="not ext">
                    					 	<img src="/static/images/cancel-icon.png"/>
                    					</td>
                    				</tr>
                    			</table>
                    		</td>
                    	</tr>
                    </table>
                    
                    <div class="toolbar">
	                    <table border='0' cellpadding='0' cellspacing='0' width="100%">
	    					<tr>
	    						<td width="100%" align="right">
	                                <button type="button" onclick="save_file(form)">Save</button>
	                            </td>
	                            <td>
	                                <button type="button" onclick="history.back()">Cancel</button>
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
