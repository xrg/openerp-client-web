<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="tinyerp/templates/master.kid">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Drop Database</title>
 </head>

<body>
	<div class="view">
    	<div class="box2 welcome">Drop Database</div>
		<form action="/dbadmin/drop" method="post">
            <div align="center" class="box2">
				<table align="center" width="100%">
					<tr>
						<td align="right" width="90" class="label">Database :</td>
						<td>
							<select name="db_name" style="width: 100%;">
								<span py:for="db in dblist">
									<option py:content="db" py:if="db == selectedDb" selected="true">dbname</option>
									<option py:content="db" py:if="db != selectedDb">dbname</option>
								</span>
							</select>
						</td>
					</tr>
					<tr>
						<td align="right" width="90" class="label">Password :</td>
						<td><input type="password" name="passwd" id="user" style="width: 99%;" /></td>
					</tr>
				</table>
            </div>					
				
			<div align="right" class="box2">
                <button type="button" onclick="window.location.href='/dbadmin'">Cancel</button>
                <button type="submit">OK</button>
            </div>
		</form>		
		<div class="box message" id="message" py:if="message" py:content="message"/>
	</div>
</body>
</html>
