<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="tinyerp/templates/master.kid">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Admin Password</title>
 </head>

<body>
	<div class="view">
		<div class="header">
			<div class="title">
				<table width="100%">
					<tr>
						<td>
							Change Password
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
						<td align="right" width="90" class="label">Host :</td>
						<td>
							${host}:${port}
						</td>
					</tr>
				</table>
			</div>
			<div align="center" class="box2">
				<form action="/dbadmin/password" method="post">
				<input type="hidden" name="host" value="${host}" />
				<input type="hidden" name="port" value="${port}" />
					<table align="center" width="100%">
						<tr>
							<td align="right" width="99" class="label">Old Password :</td>
							<td><input type="password" name="old_passwd" id="user" style="width: 99%;" /></td>
						</tr>
						<tr>
							<td align="right" width="99" class="label">New Password :</td>
							<td><input type="password" name="new_passwd" id="user" style="width: 99%;" /></td>
						</tr>
						<tr>
							<td align="right" width="99" class="label">Confirm Password :</td>
							<td><input type="password" name="new_passwd2" id="user" style="width: 99%;" /></td>
						</tr>
						<tr>
							<td>
							</td>
							<td align="right">
								<input type="submit" name="submit" value="Ok" />
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
