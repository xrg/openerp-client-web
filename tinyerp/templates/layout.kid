<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python from tinyerp import rpc ?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="master.kid">

<head py:match="item.tag=='{http://www.w3.org/1999/xhtml}head'" py:attrs="item.items()">
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title py:replace="''">Your title goes here</title>
    <meta py:replace="item[:]"/>
	<link href="/static/css/style.css" rel="stylesheet" type="text/css" />

	<script language="javascript" src="/tg_static/js/MochiKit.js"></script>
	<script language="javascript" src="/static/javascript/master.js"></script>
</head>

<body py:match="item.tag=='{http://www.w3.org/1999/xhtml}body'" py:attrs="item.items()">

<table border="0" cellpadding="0" cellspacing="5px" id="container">
  <tbody>
    <tr>
        <td colspan="2" rowspan="1" id="header">
            <table border="0" cellpadding="0" cellspacing="0" width="100%" height="100%">
                <tr>
                    <td id="titlebar">
						<h1>Welcome to eTiny!</h1>
                    </td>
                </tr>
                <tr>
                    <td id="linkbar">
                        <span py:if="rpc.session.is_logged()">
							Welcome ${rpc.session.fullname}
							|
							<a href="/pref/create/" target="contentpane">Preferences</a>
							|
							${str(rpc.session.url).rstrip('/xmlrpc')}
							|
							<a href="/logout">LOGOUT</a>
						</span>
                    </td>
                </tr>
            </table>
        </td>
    </tr>

    <tr>
        <td height="100%">
            <table py:replace="[item.text]+item[:]"/>
        </td>
    </tr>

    <tr>
      <td colspan="2" rowspan="1" id="footer">Copyright &copy; 2007 <a href="http://tinyerp.com" target="top">TinyERP Pvt Ltd.</a> All Rights Reserved.</td>
    </tr>

  </tbody>
</table>

</body>
</html>
