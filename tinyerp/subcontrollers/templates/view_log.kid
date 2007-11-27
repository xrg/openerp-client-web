<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="../../templates/master.kid">
<head>
    <title>Information</title>
    <link href="/static/css/style.css" rel="stylesheet" type="text/css"/>
</head>
<body>
    <table class="view" cellspacing="5" border="0" width="100%">
        <tr>
            <td>
                <table width="100%" class="titlebar">
                    <tr>                        
                        <td width="100%">Information</td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td>              
                <div class="box2">
                    <table border="0" width="100%" align="center">
	                    <tr py:for="key, val in todo">	                    
	                        <td class="label" py:if="key in tmp">
	                            ${val} :	                               	                        
                            </td>
                            <td>
                                ${tmp[key]}                  
                            </td>
                        </tr>
	                </table>                
	            </div>
                <div class="toolbar">
		            <table border="0" cellpadding="0" cellspacing="0" width="100%">
		                <tr>
		                    <td width="100%">
		                    </td>
		                    <td>
		                        <button type="button" onclick="window.close()">Ok</button>
		                    </td>
		                </tr>
		            </table>
		        </div>
            </td>
        </tr>
    </table>    
</body>
</html>