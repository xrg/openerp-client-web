<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends='layout.kid'>
<head>
	<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
	<title>Welcome to Web Client for TinyERP</title>	
</head>
<body>

	<table border="0" cellpadding="0" cellspacing="0" width="100%" height="100%">
		<tr>
			<td id="sidebar">
			
				<table border="0" cellpadding="0" cellspacing="0" width="100%" height="100%">
					<tr>
						<td class="title">Menu</td>
					</tr>
					<tr>
						<td valign="top" height="100%" width="100%">	
							<div class="scrollbox">
								${menu_tree.display()}		
							</div>
						</td>
					</tr>
				</table>					
			</td>
			
			<td height="100%" width="10px" align="center"><div class="vline"></div></td>
			
			<td id="content">
				<iframe id="contentpane" name="contentpane" width="100%" height="100%" frameborder="0">
				</iframe>
			</td>
		</tr>
    </table>
        
</body>
</html>
