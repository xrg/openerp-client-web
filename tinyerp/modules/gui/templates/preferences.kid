<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python import sitetemplate ?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="sitetemplate">
<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <link href="/static/css/style.css" rel="stylesheet" type="text/css" />
    <script language="javascript" src="/tg_static/js/MochiKit.js"></script>
    <script language="javascript" src="/static/javascript/master.js"></script>
    <title>Prefernces</title>

</head>
<body>
<form action="/pref/ok" method="post">
<div class="view">

    <div class="header">

        <div class="title">
            Preferences
        </div>

        <div class="spacer"></div>
    </div>
	<div class="box">
		<table align="center" width="100%">
			<tr>
				<td align="right" width="90">Language :</td>
				<td>
					${field.display()}
				</td>
			</tr>
			<tr>
			</tr>
			<tr>
			<td>
			</td>
			<td align="right">
					<input type='submit' value="Ok" onclick="form.target = window.parent;" />
					<input type='submit' name='cancel' value='Cancel' onclick="form.target=null"/>
			</td>

			</tr>
		</table>
	</div>
</div>
</form>
</body>
</html>
