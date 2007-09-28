<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="tinyerp/templates/master.kid">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Database Backup</title>
</head>

<body>
    <div class="view">
		<div class="box2 welcome">Backup Database</div>
		<form name="backup" action="/dbadmin/backup" method="post">	        
	        <div class="box2" align="center">
				<table align="center" border="0" width="100%">
					<tr>
		                <td align="right" class="label" nowrap="nowrap">
		                    Password :
		                </td>
		                <td class="item" width="100%">
		                    <input type="password" name="password" style="width: 99%;"/>
		                </td>
		            </tr>
		            <tr>
			            <td align="right" class="label" nowrap="nowrap">
	                        Databases :
		                </td>
		                <td class="item" width="100%">
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
                            <button type="button" onclick="window.location.href='/dbadmin'">Cancel</button>
                            <button type="submit">OK</button>
	                    </td>
		            </tr>
		        </table>
		    </div>

	        <div class="box message" id="message" py:if="message" py:content="message"/>
        </form>
    </div>

</body>
</html>
