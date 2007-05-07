<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="master.kid">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Login</title>

    <script type="text/javascript">
    <!--
        function setfocus() {
            var active = $('host');
            active = active ? active : ($('user').value ? $('passwd') : $('user'));
            active.focus();
    	}

		connect(window, "onload", setfocus);
	-->
    </script>

 </head>

<body>
	<span py:match="item.tag=='{http://www.w3.org/1999/xhtml}span'">
	</span>


	<div class="view">

		<form action="${target}" method="post" name="loginform" class="loginbox">

    		<input type="hidden" py:for="key, value in origArgs.items()" name="${key}" value="${str(value)}"/>

			<table align="center" width="100%" cellspacing="5px" id="hostinfo" py:if="action == 'change' or dblist is -1">

				<tr>
					<td class="label">Host :</td>
					<td><input type="text" id="host" name="host" value="${host}" style="width: 100%"/></td>
				</tr>
				<tr>
					<td class="label">Port:</td>
					<td><input type="text" id="port" name="port" value="${port}" style="width: 100%"/></td>
				</tr>
				<tr>
				    <td class="label">Protocol connection:</td>
				    <td>
				        <select id="protocol" name="protocol" style="width: 100%">
				            <option value="http" selected="${tg.selector(protocol=='http')}">XML-RPC</option>
				            <option value="https" selected="${tg.selector(protocol=='https')}">XML-RPC (secure)</option>
				            <option value="socket" selected="${tg.selector(protocol=='socket')}">NET-RPC (faster)</option>
				        </select>
				    </td>
				</tr>
				<tr>
				    <td colspan="2" align="right">
				        <button type="submit" name="login_action" value="connect">Connect</button>
				    </td>
				</tr>
			</table>

		    <table align="center" width="100%" cellspacing="5px" py:if="action != 'change' and dblist is not -1">
		        <input type="hidden" name="host" value="${host}"/>
		        <input type="hidden" name="port" value="${port}"/>
		        <input type="hidden" name="protocol" value="${protocol}"/>
		        <input type="hidden" name="login_action" value="login"/>

		        <tr>
		            <td class="label">Host :</td>
		            <td width="250px">
		                <input value="${protocol}://${host}:${port}" style="width: 100%" disabled="0"/>
                    </td>
                    <td>
					    <button type="button" onclick="form.login_action.value='change'; form.submit()">Change</button>
					</td>
		        </tr>

				<tr>
					<td class="label">Database :</td>
					<td>
						<select name="db" style="width: 100%;">
							<option py:for="v in dblist or []" py:content="v" selected="${tg.selector(v==db)}">dbname</option>
                        </select>
					</td>
                    <td>
					    <button type="button" onclick="location.href='/dbadmin'">Manage</button>
					</td>
				</tr>

				<tr>
					<td class="label">User :</td>
					<td colspan="2"><input type="text" id="user" name="user" style="width: 99%;" value="${user}"/></td>
				</tr>
				<tr>
					<td class="label">Password :</td>
					<td colspan="2"><input type="password" id="passwd" name="passwd"  style="width: 99%;"/></td>
				</tr>
				<tr>
				    <td></td>
				    <td></td>
					<td>
						<button type="submit" style="width: 100%">Login</button>
					</td>
				</tr>

			</table>

		</form>

		<div class="box message" id="message" py:if="message">
		    ${message}
        </div>

    </div>

</body>

</html>
