<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="tinyerp/templates/master.kid">
<head>
    <title>Prefernces</title>
</head>
<body>

<div class="view">
    <div class="header">
        <div class="title">Preferences</div>
        <div class="spacer"></div>
    </div>
    
	<div class="box">
		<form action="/pref/ok" method="post">
			<table align="center" width="100%">
				<tr>
					<td align="right" width="90">Language :</td>
					<td>
						${field.display()}
					</td>
				</tr>
				<tr>
				</tr>
				<tr>
				<td>
				</td>
				<td align="right">
						<input type='submit' value="OK" onclick="form.target='_top'" />
						<button type='button' onclick="history.back()">Cancel</button>
				</td>
	
				</tr>
			</table>
		</form>
	</div>
	
</div>

</body>
</html>
