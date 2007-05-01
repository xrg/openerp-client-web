<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python import sitetemplate ?>
<?python from tinyerp import rpc ?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="sitetemplate">

<head py:match="item.tag=='{http://www.w3.org/1999/xhtml}head'" py:attrs="item.items()">
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    
    <meta py:replace="item[:]"/>
	<link href="/static/css/style.css" rel="stylesheet" type="text/css" />

    <title py:replace="''">Your title goes here</title>
    
	<script language="javascript" src="/tg_static/js/MochiKit.js"></script>
	<script language="javascript" src="/static/javascript/master.js"></script>
</head>

<body py:match="item.tag=='{http://www.w3.org/1999/xhtml}body'" py:attrs="item.items()">

<div id="container">

    <div id="header">
        <table border="0" cellpadding="0" cellspacing="0" width="100%" height="100%">
            <tr>
                <td id="titlebar">
       				<div style="font-size: 22px; font-style: oblique; font-weight: bold; margin-bottom: 5px">Welcome to Tiny ERP</div>
       				<div style="position: absolute; left: 100px;">
                        <i>Developped by:</i> <a href="http://axelor.com">Axelor</a> &amp; <a href="http://tinyerp.com">Tiny sprl</a>.
                    </div>
                </td>
            </tr>
            <tr>
                <td id="linkbar">
                    <span py:if="rpc.session.is_logged()">
						Welcome ${rpc.session.fullname}
						|
						<a href="/pref/create/" target="_blank">Preferences</a>
						|
						${str(rpc.session.url).rstrip('/xmlrpc')}
						|
						<a href="/">HOME</a>
						|
						<a href="/logout">LOGOUT</a>
					</span>
                </td>
            </tr>
        </table>
    </div>

    <div py:replace="[item.text]+item[:]"/>
    
    <div id="footer">
        <table border="0" cellpadding="0" cellspacing="0" width="100%">            
            <tr>
                <td align="right">
                    &copy; 2007 <a href="http://tinyerp.com" target="top">Tiny ERP.</a> All Rights Reserved.<br/>
                    &copy; 2007 <a href="http://axelor.com" target="top">Axelor.</a> All Rights Reserved.
                </td>
            </tr>
        </table>
    </div>

</div>

</body>
</html>
