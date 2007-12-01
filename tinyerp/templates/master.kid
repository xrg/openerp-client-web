<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python import sitetemplate ?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="sitetemplate">

<head py:match="item.tag=='{http://www.w3.org/1999/xhtml}head'" py:attrs="item.items()">
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <meta py:replace="item[:]"/>

    <link href="/static/css/style.css" rel="stylesheet" type="text/css"/>
    <link href="/static/css/icons.css" rel="stylesheet" type="text/css"/>
    <link href="/static/css/menu.css" rel="stylesheet" type="text/css"/>

    <!--[if lt IE 7]>
        <link href="/static/css/iepngfix.css" rel="stylesheet" type="text/css"/>
    <![endif]-->

    <!--[if lt IE 7]>
    <style type="text/css">
        ul.tabbernav {
        padding: 0px;
    }

    ul.tabbernav li {
        left: 10px;
        top: 1px;
    }
    </style>
    <![endif]-->

    <!--[if IE]>
        <link href="/static/css/style-ie.css" rel="stylesheet" type="text/css"/>
    <![endif]-->

    <title py:replace="''">Your title goes here</title>
    <script type="text/javascript" src="/static/javascript/master.js"></script>
    <script type="text/javascript" src="/static/javascript/menu.js"></script>
    <script type="text/javascript" src="/static/javascript/ajax.js"></script>
</head>

<body py:match="item.tag=='{http://www.w3.org/1999/xhtml}body'" py:attrs="item.items()">

<?python
shortcuts = tg.root.shortcuts.my()
requests, requests_message = tg.root.requests.my()
?>

<table id="container" border="0" cellpadding="0" cellspacing="0">
    <tr py:if="value_of('show_header_footer', True)">
           <td>
            <table id="header" class="header" cellpadding="0" cellspacing="0" border="0">
                <tr>
                    <td rowspan="2">
                        <img src="/static/images/tinyerp_big.png" alt="${_('Tiny ERP Logo')}" border="0" width="205px" height="58px" usemap="#logo_map"/>
                        <map name="logo_map">
                            <area shape="rect" coords="90,39,124,54" href="http://tinyerp.com" target="_blank"/>
                            <area shape="rect" coords="131,38,172,54" href="http://axelor.com" target="_blank"/>
                        </map>
                    </td>
                    <td align="right" valign="top" nowrap="nowrap">
                        <table class="menu_connection" cellpadding="0" cellspacing="0" border="0">
                            <tr>
                                <td>
                                    <img src="/static/images/tinyerp_small.png" title="Tiny ERP - Open Source Management Soution" border="0" width="84" height="24"/>
                                </td>
                                <td width="26" style="background: transparent url(/static/images/diagonal_right.gif) no-repeat scroll right;" nowrap="nowrap">
                                    <div style="width: 26px;"/>
                                </td>
                                <td class="menu_connection_welcome" nowrap="norwap">Welcome <span>${rpc.session.user_name or 'guest'}</span></td>
                                <td class="menu_connection_links" nowrap="norwap">
                                    <a href="/">Home</a>
                                    <a href="/pref/create/">Preferences</a>
                                    <a href="/about">About</a>
                                    <a href="/logout">Logout</a>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
                <tr>
                    <td align="right" valign="middle">
                        <div py:if="rpc.session.is_logged()">
                            Requests: <a href="${tg.query('/requests', ids=requests)}">${requests_message}</a>&nbsp;&nbsp;
                        </div>
                    </td>
                </tr>
                <tr>
                    <td colspan="2" nowrap="nowrap">

                        <table width="100%" cellspacing="0" cellpadding="0" id="menu_header" >
                            <tr>
                                <td width="5%" id="menu_header_menu" nowrap="nowrap">
                                    <a href="/menu">MAIN MENU</a>
                                </td>
                                <td width="5%" id="menu_header_shortcuts" nowrap="nowrap">
                                    <a href="/shortcuts">SHORTCUTS</a>
                                </td>
                                <td width="26" style="background: transparent url(/static/images/diagonal_left.gif) no-repeat scroll left;" nowrap="nowrap"/>
                                <td py:if="rpc.session.is_logged()" nowrap="nowrap">
                                    <table id="shortcuts" class="menubar" border="0" cellpadding="0" cellspacing="0">
                                        <tr>
                                            <td py:for="i, sc in enumerate(shortcuts)" py:if="i&lt;6" nowrap="nowrap">
                                                <a href="${tg.query('/tree/open', id=sc['res_id'], model='ir.ui.menu')}">${sc['name']}</a>
                                            </td>
                                            <td py:if="len(shortcuts) &gt; 6" id="shortcuts_menu" nowrap="nowrap">
                                                <a href="javascript: void(0)">>></a>
                                                <div class="submenu" id="shortcuts_submenu">
                                                    <table cellpadding="0" cellspacing="1">
                                                        <tr py:for="sc in shortcuts[6:]">
                                                            <td><a href="${tg.query('/tree/open', id=sc['res_id'], model='ir.ui.menu')}">${sc['name']}</a></td>
                                                        </tr>
                                                    </table>
                                                </div>
                                            </td>
                                        </tr>
                                    </table>
                                    <script type="text/javascript" py:if="len(shortcuts) &gt; 6">
                                        new Menu('shortcuts_menu', 'shortcuts_submenu');
                                    </script>
                                </td>
                                <td>
                                    &nbsp;
                                </td>
                                <td align="right">
                                    <a  py:if="tg.root.shortcuts.can_create()" href="${tg.query('/shortcuts/add', id=rpc.session.active_id)}" id="menu_header">[ADD]</a>
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
    <tr py:if="value_of('show_header_footer', True)">
        <td>
            <div id="footer">
            <br/>
            <hr/>
            (C) Copyright 2006-Today, Tiny ERP Pvt Ltd. More Information on <a id="footer" href="http://tinyerp.com">http://tinyerp.com</a>.<br/>
            The web client is developed by Axelor (<a id="footer" href="http://axelor.com">http://axelor.com</a>) and Tiny (<a id="footer" href="http://tiny.be">http://tiny.be</a>)<br/>
            Running Server: <span>http://${rpc.session.host}:${rpc.session.port} - database:${rpc.session.db}</span><br/>
            </div>
        </td>
    </tr>
</table>

</body>
</html>
