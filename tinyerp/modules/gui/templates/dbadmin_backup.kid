<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="tinyerp/templates/master.kid">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Login</title>
</head>

<body>
    <div class="view">
		<div class="header">
			<div class="title">
				<table width="100%">
					<tr>
						<td>
							Backup Database
						</td>
						<td align="right">
							<a href="/dbadmin?host=${host}&amp;port=${port}">Cancel</a>
						</td>
					</tr>
				</table>
			</div>
		</div>

		<div class="spacer"></div>

		<div class="content">
			<form name="backup" action="/dbadmin/backup" method="post">
	            <input type="hidden" name="host" value="${host}" />
			    <input type="hidden" name="port" value="${port}" />

			        <div class="box2">
						<table align="center" border="0" width="100%">
							<tr>
								<td align="right" width="90">Host :</td>
								<td>
									${host} :${port}
								</td>
							</tr>
						</table>
				    </div>

			        <div class="box2" id="create">
						<table align="center" border="0" width="100%">
							<tr>
				                <td align="right">
				                    Password :
				                </td>
				                <td>
				                    <input type="password" name="password" style="width: 99%;"/>
				                </td>
				            </tr>
				            <tr>
					            <td align='right'>
			                        Databases :
				                </td>
				                <td>
				                    <select name="dblist" style="width: 100%;">
	    		                        <span py:for="db in dblist">
		    	                            <option py:content="db" py:if="db == selectedDb" selected="true">Database</option>
											<option py:content="db" py:if="db != selectedDb">Database</option>
			                            </span>
			                        </select>
			                    </td>
			                </tr>
						</table>
					</div>

	                <div class="box2">
						<table align="center" border="0" width="100%">
		                    <tr>
				                <td></td>
				                <td align="right">
			                        <input type="submit" name="submit" value="Save"/>
			                    </td>
				            </tr>
				        </table>
				    </div>

		        <div class="box message" id="message" py:if="message">
	                ${message}
	    		</div>
	        </form>
		</div>
    </div>

</body>
</html>
