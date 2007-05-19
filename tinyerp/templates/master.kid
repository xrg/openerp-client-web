<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python import sitetemplate ?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="sitetemplate">

<head py:match="item.tag=='{http://www.w3.org/1999/xhtml}head'" py:attrs="item.items()">
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>

    <meta py:replace="item[:]"/>

	<link href="/static/css/style.css" rel="stylesheet" type="text/css" />
	<link href="/static/css/icons.css" rel="stylesheet" type="text/css" />
	<link href="/static/css/tabs.css" rel="stylesheet" type="text/css" />

    <title py:replace="''">Your title goes here</title>

	<script type="text/javascript" src="/tg_static/js/MochiKit.js"></script>
	<script type="text/javascript" src="/static/javascript/master.js"></script>
</head>

<body py:match="item.tag=='{http://www.w3.org/1999/xhtml}body'" py:attrs="item.items()">

<table id="container" border="0" cellpadding="0" cellspacing="0">
	<tr>
    	<td>    	    
	    	<table id="header" class="header" height="65" cellpadding="0" cellspacing="0">
				<tr>
					<td rowspan="2">
						<a href="http://www.tinyerp.com" class="imglink"><img src="/static/images/tiny_good.png" alt="Tiny ERP logo" border="0"/></a>
					</td>
					<td align="right" valign="top" py:if="rpc.session.is_logged()">
						<table class="menu_connection" cellpadding="0" cellspacing="0">
							<tr height="">
								<td><img src="/static/images/corner.gif" alt="\"/></td>
								<td class="menu_connection_welcome" >Welcome ${rpc.session.user_name}</td>
								<td class="menu_connection">
									<a class="menu_connection" href="/">Home</a> &nbsp;
									<a class="menu_connection" href="/pref/create/">Preferences</a> &nbsp;
									<a class="menu_connection" href="">About</a> &nbsp;
									<a class="menu_connection" href="/logout">Logout</a>
								</td>
							</tr>
						</table>
					</td>
				</tr>
				<tr>
					<td align="right" valign="Top">
						<a py:def="requests(ids)" href="${tg.query('/requests', ids=ids)}">${len(ids)}</a>
	                    <div py:if="rpc.session.is_logged()">
                            Requests: ${requests(tg.root.requests.my()[0])} &nbsp; &nbsp;<button>NEW</button> &nbsp;
                        </div>
					</td>
				</tr>
				<tr>
                    <td colspan="2">

						<table width="100%" cellspacing="0" cellpadding="0" class="menu_header" >
							<tr>
								<td width="100" id="menu_header_menu" background="/static/images/mainmenu_button.png">
									<a id="menu_header" href="/">MAIN MENU</a>
								</td>
								<td width="90" id="menu_header_shortcuts" >
									<a id="menu_header" href="/shortcuts">SHORTCUTS</a>
								</td>
								<td width="35">
									<img src="/static/images/head_diagonal.png" alt="\"/>
								</td>
								<td>
									<span py:for="sc in tg.root.shortcuts.my()">
			                        	<a id="menu_header"  href="${tg.query('/tree/open', id=sc['res_id'], model='ir.ui.menu')}">
			                        		${sc['name']}
			                        	</a>
			                        	<font color="white">&nbsp;|&nbsp;</font>
			                        </span>
								</td>
								<td align="right">
										<a  py:if="rpc.session.is_logged() and rpc.session.active_id" href="${tg.query('/shortcuts/add', id=rpc.session.active_id)}" id="menu_header">[ADD]</a>
										&nbsp;
								</td>
							</tr>
						</table>
			
			        </td>
                </tr>
            </table>
        </td>
    </tr>
    <tr>
        <td>
            <div py:replace="[item.text]+item[:]"/>
        </td>
    </tr>
    <tr>
        <td>
	        <div id="footer">
			<br/>
			<hr/>
			(C) Copyright 2006-Today, Tiny ERP Pvt Ltd. More Information on <a id="footer" href="http://tinyerp.com">http://tinyerp.com</a>.<br/>
			The web client is developed by Axelor (<a id="footer" href="http://axelor.com">http://axelor.com</a>) and Tiny (<a id="footer" href="http://tiny.be">http://tiny.be</a>)<br/>
			Running Server: http://${rpc.session.host}:${rpc.session.port} - database:${rpc.session.db}<br/>
			</div>
        </td>
    </tr>
</table>

</body>
</html>
