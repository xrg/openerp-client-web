<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="tinyerp/templates/master.kid">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Restore Database</title>
 </head>

<body>
	<div class="view">
		<div class="header">
			<div class="title">
				<table width="100%">
					<tr>
						<td>
							Restore Database
						</td>
						<td align="right">
							<a href="/dbadmin?host=${host}&amp;port=${port}">Cancel</a>
						</td>
					</tr>
				</table>
			</div>
		</div>
		<div class="spacer"></div>
		<div id="content">
			<div class="box2">
				<table align="center" border="0" width="100%">
					<tr>
						<td align="right" width="90" class="label">Host:</td>
						<td>
							${host}:${port}
						</td>
					</tr>
				</table>
			</div>
			<div align="center" class="box2">
				<form action="/dbadmin/restore" method="post" enctype="multipart/form-data">
				<input type="hidden" name="host" value="${host}" />
				<input type="hidden" name="port" value="${port}" />
					<table align="center" width="100%">
						<tr>
							<td align="right" width="99" class="label">File :</td>
							<td ><input type="file" name="path" id="path"/></td>
						</tr>
						<tr>
							<td align="right" width="90" class="label">Password :</td>
							<td><input type="password" name="passwd" id="passwd" style="width: 99%;" /></td>
						</tr>
						<tr>
							<td align="right" width="90" class="label">New Database name :</td>
							<td><input type="text" name="new_db"  style="width: 99%;" /></td>
						</tr>
						<tr>
							<td>
							</td>
							<td align="right">
								<input type="submit" name="submit" value="Restore" />
							</td>
						</tr>
					</table>
				</form>
			</div>
			<div class="box message" id="message" py:if="message">
				${message}
			</div>
		</div>
	</div>
</body>
</html>
