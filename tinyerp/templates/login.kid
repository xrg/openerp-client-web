<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="master.kid">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Login</title>
 </head>

<body>

<?python
display1 = 'table'
display2 = 'table'

if action == 'change' or dblist is None:
    display2 = 'none'
else:
    display1 = 'none'    
    
?>

	<div class="view">
		    
		<form action="${target}" method="post">				
		
    		<input type="hidden" py:for="key, value in origArgs.items()" name="${key}" value="${str(value)}"/>
    		    		
			<table align="center" class="loginbox" cellspacing="5px" style="display: ${display1}">

				<tr>
					<td class="label">Host :</td>
					<td><input type="text" name="host" value="${host}" style="width: 100%"/></td>
				</tr>
				<tr>
					<td class="label">Port:</td>
					<td><input type="text" name="port" value="${port}" style="width: 100%"/></td>    					
				</tr>
				<tr>
				    <td class="label">Protocol connection:</td>
				    <td>
				        <select name="protocol" style="width: 100%"> 				            
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
		
		    <table align="center" class="loginbox" cellspacing="5px" style="display: ${display2}">

			        <tr>
			            <td class="label">Host :</td>
			            <td width="250px">
			                <input value="${protocol}://${host}:${port}" style="width: 100%" disabled="0"/>
                        </td>
                        <td>
						    <button type="submit" name="login_action" value="change">Change</button>
						</td>
			        </tr>	
			        
					<tr>
						<td class="label">Database :</td>
						<td colspan="2">
							<select name="db" style="width: 100%;">
								<option py:for="v in dblist or []" py:content="v" selected="${tg.selector(v==db)}">dbname</option>
                            </select>
						</td>
					</tr>

					<tr>
						<td class="label">User :</td>
						<td colspan="2"><input type="text" name="user" id="user" style="width: 99%;" value="${user}"/></td>
					</tr>
					<tr>
						<td class="label">Password :</td>
						<td colspan="2"><input type="password" name="passwd"  style="width: 99%;"/></td>
					</tr>
					<tr>
						<td colspan="3" align="right">
							<button type="submit" name="login_action" value="login">Log In</button>
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
