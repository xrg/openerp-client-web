<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="tinyerp/templates/master.kid">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Database Admin</title>
 </head>
<body>
	<div class="view">
		<div class="header">
			<div class="title">
				<table width="100%">
					<tr>
						<td>
							Database Administration
						</td>
						<td align="right">
							<a href="/">BACK</a>
						</td>
					</tr>
				</table>
			</div>
		</div>
		<div class="spacer"></div>
  		<div id="content">
  			<div class="box">
				<table align="center" border="0" width="100%">
					<tr>
						<td align="center"><a href="/dbadmin/create">Create</a></td>
						<td align="center"><a href="/dbadmin/drop">Drop</a></td>
						<td align="center"><a href="/dbadmin/backup">Backup</a></td>
						<td align="center"><a href="/dbadmin/restore">Restore</a></td>
						<td align="center"><a href="/dbadmin/password">Password</a></td>
					</tr>
				</table>
			</div>
		</div>
	</div>
</body>
</html>
