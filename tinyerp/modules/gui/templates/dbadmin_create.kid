<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="tinyerp/templates/master.kid">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Login</title>
    
</head>

<body onload="hideElement('showbar')">
    <div class="view">
		<div class="header">
			<div class="title">
				<table width="100%">
					<tr>
						<td>
							Create Database
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

			<form action="/dbadmin/create" method="post" name="create">
			<input type="hidden" name="host" value="${host}" />
			<input type="hidden" name="port" value="${port}" />

	            <div class="box2">
					<table align="center" border="0" width="100%">
						<tr>
							<td align="right" width="90" class="label">Host :</td>
							<td>
								${host} :${port}
							</td>
						</tr>
					</table>
				</div>


	            <div class="box2" id="create">
					<table align="center" border="0" width="100%">
						<tr>
			                <td align="right" class="label">
			                    Super admin password :
			                </td>
			                <td>
			                    <input type="password" name="password" style="width: 99%;"/>
			                </td>
			            </tr>
			            <tr>
			                <td></td>
			                <td>
			                    (use 'admin', if you did not changed it)
			                </td>
			            </tr>

				        <tr>
			                <td align="right" class="label">
			                    New database name :
			                </td>
			                <td>
			                    <input type="text" name="db_name" style="width: 99%;"/>
			                </td>
			            </tr>
			            <tr>
			                <td align='right' class="label">
			                    Load Demonstration data :
			                </td>
			                <td>
			                    <input type="checkbox" name="demo_data" checked="true"/>
			                </td>
			            </tr>
			            <tr>
			                <td align='right' class="label">
			                    Initialize Database :
			                </td>
			                <td>
			                    <input type="checkbox" name="db_init" checked="true"/>
			                </td>
			            </tr>
			            <tr>
			                <td align='right' class="label">
			                    Default Language :
			                </td>
			                <td>
			                    <select name="language" style="width: 100%;">
		                            <option py:for="i, key in enumerate(langlist)" value="${langlist[i][0]}" py:content="langlist[i][1]" selected="${(i+1 == len(langlist) or None) and 1}">Language</option>
			                    </select>
			                </td>
			            </tr>
			        </table>

				</div>

				<div align="right" class="box2">
                    <input type="submit" name="submit" value="Create"/>
        		</div>
        		
				<div class="box message" id="message" py:if="message">
                    ${message}
        		</div>
        </form>
		</div>
    </div>

</body>
</html>
