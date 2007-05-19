<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="master.kid">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Login</title>
</head>

<body>
	<div class="view">
	    <div class="box2 welcome">
	        Welcome to Tiny ERP
	    </div>
	    <div class="box2">
			<form action="${target}" method="post" name="loginform">
		        <input type="hidden" py:for="key, value in origArgs.items()" name="${key}" value="${str(value)}"/>
		        <input type="hidden" name="login_action" value="login"/>
	                
	    		<table align="center" width="100%" cellspacing="5px">
			        <tr>
			            <td class="label">Host :</td>
			            <td width="100%">
			                ${url} 
			            </td>
			        </tr>
			        <tr>
						<td class="label">Database :</td>
						<td width="100%">
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
						<td colspan="2"><input type="password" value="" id="passwd" name="passwd" style="width: 99%;"/></td>
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
		</div>

		<div class="box message" id="message" py:if="message">
		    ${message}
        </div>
    </div>
</body>

</html>
