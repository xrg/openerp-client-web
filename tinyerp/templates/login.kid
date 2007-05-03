<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="master.kid">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Login</title>
    
    <script type="text/javascript">
    <!--
        function setfocus() {
                                
                var host = document.getElementsByName('host');
                var user = document.getElementsByName('user');
                
                if (host && host[0])
                    host[0].focus();                   
                    
                if (user && user[0])
                    user[0].focus();
    	}

		function submit_form(action){
		
		    var form = document.loginform;
		    form.login_action = action;
		    
		    form.submit();
		}
		
		connect(window, "onload", setfocus);
	-->
    </script>
    
 </head>

<body>

	<div class="view">
		    
		<form action="${target}" method="post" name="loginform">				
		
    		<input type="hidden" py:for="key, value in origArgs.items()" name="${key}" value="${str(value)}"/>
    		    		
			<table align="center" class="loginbox" cellspacing="5px" id="hostinfo" py:if="action == 'change' or dblist is None">

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
		
		    <table align="center" class="loginbox" cellspacing="5px" py:if="action != 'change' and dblist is not None">
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
						<button type="submit">Log In</button>
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
