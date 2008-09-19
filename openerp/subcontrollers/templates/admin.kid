<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="../../templates/master.kid">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Config Editor</title>
        
</head>

<body>
    <div class="view">
        <table width="100%" class="titlebar">
            <tr>
                <td width="32px" align="center">
                    <img src="/static/images/icon.gif"/>
                </td>
                <td width="100%">Administration</td>
            </tr>
        </table>
        <table width="100%">
            <tr>
                <td width="20%" valign="top" py:if="not mode=='authorize'">
                    <table>
                        <tr>
                            <td width="100%" valign="top" id="sidebar">
                                <table cellpadding="0" cellspacing="0" border="0" class="sidebox" width="100%">
                                    <tr>
                                        <td>
                                            <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                                <tr>
                                                    <td width="8" style="background: #ac0000"/>
                                                    <td width="7" style="background-color: #363636"/>
                                                    <td style="font: verdana; color:white; font-weight:bold; font-size:12px; background-color: #363636">Server Admin</td>
                                                    <td width="25" valign="top" style="background: url(/static/images/diagonal_left.gif) no-repeat; background-color: #666666"/>
                                                    <td width="50" style="background-color: #666666"/>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            <a href="#" onclick="window.location.href='/admin?id=db_config'">Configuration</a>
                                        </td>
                                    </tr>
                                </table>
                            </td>                                
                        </tr>
                        <tr>
                            <td width="100%" valign="top" id="sidebar">
                                <table cellpadding="0" cellspacing="0" border="0" class="sidebox" width="100%">
                                    <tr>
                                        <td>
                                            <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                                <tr>
                                                    <td width="8" style="background: #ac0000"/>
                                                    <td width="7" style="background-color: #363636"/>
                                                    <td style="font: verdana; color:white; font-weight:bold; font-size:12px; background-color: #363636">DB Admin</td>
                                                    <td width="25" valign="top" style="background: url(/static/images/diagonal_left.gif) no-repeat; background-color: #666666"/>
                                                    <td width="50" style="background-color: #666666"/>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            <a href="#" onclick="window.location.href='/admin?id=db_create'">Create</a>
                                        </td>
                                    </tr><tr>
                                        <td>
                                            <a href="#" onclick="window.location.href='/admin?id=db_drop'">Drop</a>
                                        </td>
                                    </tr><tr>
                                        <td>
                                            <a href="#" onclick="window.location.href='/admin?id=db_backup'">Backup</a>
                                        </td>
                                    </tr><tr>
                                        <td>
                                            <a href="#" onclick="window.location.href='/admin?id=db_restore'">Restore</a>
                                        </td>
                                    </tr><tr>
                                        <td>
                                            <a href="#" onclick="window.location.href='/admin?id=db_password'">Password</a>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                    </table>
                </td>
                <td>                
                    <div class="view" py:if="mode=='authorize'">
                        <div class="box2 welcome">Administration</div>
                        <div>
                            <form name="config" action="/admin/login" method="post">
                                <div class="box2" id="passwd">
                                    <table align="center" border="0" width="100%">
                                        <tr>
                                            <td align="right" class="label">Password :</td>
                                            <td>
                                                <input type="password" name="passwd" style="width: 99%;"/>
                                            </td>
                                        </tr>
                                    </table>
                                </div>
                                <div class="box2">
                                    <table align="center" border="0" width="100%">
                                        <tr>
                                            <td></td>
                                            <td align="right">
                                                <button type="button" onclick="window.location.href='/login'">Cancel</button>
                                                <button type="submit">OK</button>
                                            </td>
                                        </tr>
                                    </table>
                                </div>
                            </form>
                            <div class="box message" id="message" py:if="message" py:content="message"/>
                        </div>
                    </div>
                
                    <div class="view" py:if="mode=='db_config'">
                        <div class="box2 welcome">Configuration</div>
                        <div>
                            <form id="view_form" action="/admin/setconf" method="post" enctype="multipart/form-data">
                                <div class="box2" id="config">
                                    <table align="center" border="0" width="100%">
                                        <tr>
                                            <td colspan='2' class="label_header">
                                                <hr/>OpenERP Server<hr/>
                                            </td>
                                        </tr>
                                    
                                        <tr>
                                            <td align="right" class="label">Host :</td>
                                            <td>
                                                <input type="text" name="host" value="${host}" style="width: 99%;"/>
                                                <span py:if="'host' in tg.errors" class="fielderror">${tg.errors['host']}</span>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align='right' class="label">Port :</td>
                                            <td>
                                                <input type="text" name="port" value="${port}" style="width: 99%;"/>
                                                <span py:if="'port' in tg.errors" class="fielderror">${tg.errors['port']}</span>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align='right' class="label">Protocol :</td>
                                            <td>
                                                <select name="protocol" style="width: 100%;">
	                                                <span>
	                                                	<option selected="${tg.selector(protocol=='socket')}" value='socket'>NET-RPC (faster)</option>
	                                                    <option selected="${tg.selector(protocol=='http')}" value='http'>XML-RPC</option>
	                                                    <option selected="${tg.selector(protocol=='https')}" value='https'>XML-RPC secure</option>
	                                                </span>
	                                            </select>
                                                <span py:if="'protocol' in tg.errors" class="fielderror">${tg.errors['protocol']}</span>
                                            </td>
                                        </tr>
                                        
                                        <tr>
                                            <td colspan='2' class="label_header"><br/>
                                                <hr/>Company Logo<hr/>
                                            </td>
                                        </tr>
                                    
                                        <tr>
                                            <td align="right" class="label">Logo Image :</td>
                                            <td>
                                                <input type="file" id="new_logo" name="new_logo" style="width: 99%;"/>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="right" class="label">Company URL :</td>
                                            <td>
                                                <input type="text" id="comp_url" name="comp_url" value='${comp_url}' style="width: 99%;"/>
                                            </td>
                                        </tr>
                                    
                                        <tr>
                                            <td colspan='2' class="label_header"><br/>
                                                <hr/>Admin Password<hr/>
                                            </td>
                                        </tr>    
                                    
                                        <tr>
                                            <td align="right" class="label">Old Password :</td>
                                            <td>
                                                <input type="password" name="oldpwd" style="width: 99%;"/>
                                                <span py:if="'oldpwd' in tg.errors" class="fielderror">Password is Incorrect</span>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align='right' class="label">New Password :</td>
                                            <td>
                                                <input type="password" name="newpwd" style="width: 99%;"/>
                                                <span py:if="'newpwd' in tg.errors" class="fielderror">Please Enter New Password</span>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align='right' class="label">Retype Password :</td>
                                            <td>
                                                <input type="password" name="repwd" style="width: 99%;"/>
                                                <span py:if="'repwd' in tg.errors" class="fielderror">Passwords do not Match</span>
                                            </td>
                                        </tr>
                                    </table>
                                </div>
                
                                <div class="box2">
                                    <table align="center" border="0" width="100%">
                                        <tr>                            
                                            <td align="right">
                                                <button type="button" onclick="window.location.href='/admin'">Cancel</button>
                                                <button type="submit">OK</button>
                                            </td>
                                        </tr>
                                    </table>
                                </div>
                                <div class="label_header"><u>Note</u> : Any changes in configuration needs to restart the web client.</div>
                            </form>
                        </div>
                    </div>
                  
                    <div class="view" id="dbcreate" py:if="mode=='db_create'">
                        <form action="/admin/createdb" method="post">
                            <div class="box2 welcome">Create Database</div>
                            <div align="center" class="box2">
                                <table align="center" border="0" width="100%">
                                    <tr>
                                        <td align="right" class="label" nowrap="nowrap">Super admin password :</td>
                                        <td class="item" width="100%">
                                            <input type="password" name="password" style="width: 99%;"/>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td></td>
                                        <td>(use 'admin', if you did not changed it)</td>
                                    </tr>
                
                                    <tr>
                                        <td align="right" class="label" nowrap="nowrap">New database name :</td>
                                        <td class="item" width="100%">
                                            <input type="text" name="db_name" style="width: 99%;"/>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td align="right" class="label" nowrap="nowrap">Load Demonstration data :</td>
                                        <td width="100%">
                                            <input type="checkbox" class="checkbox" name="demo_data" value="True" checked="checked"/>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td align="right" class="label" nowrap="nowrap">Default Language :</td>
                                        <td class="item" width="100%">
                                            <select name="language" style="width: 100%;">
                                                <option py:for="i, key in enumerate(langlist)" value="${langlist[i][0]}" py:content="langlist[i][1]" selected="${(i+1 == len(langlist) or None) and 1}">Language</option>
                                            </select>
                                        </td>
                                    </tr>
                                </table>
                            </div>
                
                            <div align="right" class="box2">
                                <button type="button" onclick="window.location.href='/admin'">Cancel</button>
                                <button type="submit">OK</button>
                            </div>
                
                            <div class="box2 message" id="message" py:if="message">
                                <pre py:content="message"/>
                            </div>
                        </form>
                    </div>
                 
                    <div class="view" id="dbdrop" py:if="mode=='db_drop'">
                        <form action="/admin/dropdb" method="post">
                            <div class="box2 welcome">Drop Database</div>
                            <div align="center" class="box2">
                                <table align="center" width="100%">
                                    <tr>
                                        <td align="right" class="label" nowrap="nowrap">Database :</td>
                                        <td class="item" width="100%">
                                            <select name="db_name" style="width: 100%;">
                                                <span py:for="db in dblist">
                                                    <option py:content="db" py:if="db == selectedDb" selected="true">dbname</option>
                                                    <option py:content="db" py:if="db != selectedDb">dbname</option>
                                                </span>
                                            </select>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td align="right" class="label" nowrap="nowrap">Password :</td>
                                        <td class="item" width="100%"><input type="password" name="passwd" id="user" style="width: 99%;" /></td>
                                    </tr>
                                </table>
                            </div>
                
                            <div align="right" class="box2">
                                <button type="button" onclick="window.location.href='/admin'">Cancel</button>
                                <button type="submit">OK</button>
                            </div>
                        
                            <div class="box2 message" id="message" py:if="message">
                                <pre py:content="message"/>
                            </div>            
                        </form>
                    </div>
                        
                    <div class="view" id="dbbackup" py:if="mode=='db_backup'">
                        <form name="backup" action="/admin/backupdb" method="post">
                            <div class="box2 welcome">Backup Database</div>
                            <div class="box2" align="center">
                                <table align="center" border="0" width="100%">
                                    <tr>
                                        <td align="right" class="label" nowrap="nowrap">Password :</td>
                                        <td class="item" width="100%">
                                            <input type="password" name="password" style="width: 99%;"/>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td align="right" class="label" nowrap="nowrap">Databases :</td>
                                        <td class="item" py:if="dblist" width="100%">
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
                                            <button type="button" onclick="window.location.href='/admin'">Cancel</button>
                                            <button type="submit">OK</button>
                                        </td>
                                    </tr>
                                </table>
                            </div>
                
                            <div class="box2 message" id="message" py:if="message">
                                <pre py:content="message"/>
                            </div>
                        </form>
                    </div>
                
                    <div class="view" id="dbrestore" py:if="mode=='db_restore'">
                        <form action="/admin/restoredb" method="post" enctype="multipart/form-data">
                            <div class="box2 welcome">Restore Database</div>
                            <div align="center" class="box2">
                                <table align="center" width="100%">
                                    <tr>
                                        <td align="right" class="label" nowrap="nowrap">File :</td>
                                        <td class="item" width="100%"><input type="file" name="path" id="path"/></td>
                                    </tr>
                                    <tr>
                                        <td align="right" class="label" nowrap="nowrap">Password :</td>
                                        <td class="item" width="100%"><input type="password" name="passwd" id="passwd" style="width: 99%;" /></td>
                                    </tr>
                                    <tr>
                                        <td align="right" class="label" nowrap="nowrap">New Database name :</td>
                                        <td class="item" width="100%"><input type="text" name="new_db"  style="width: 99%;" /></td>
                                    </tr>
                                </table>
                            </div>
                            <div align="right" class="box2">
                                <button type="button" onclick="window.location.href='/admin'">Cancel</button>
                                <button type="submit">OK</button>
                            </div>
                        
                            <div class="box2 message" id="message" py:if="message">
                                <pre py:content="message"/>
                            </div>
                        </form>
                    </div>
                
                    <div class="view" id="dbpassword" py:if="mode=='db_password'">
                        <form action="/admin/passworddb" method="post">
                            <div class="box2 welcome">Change Password</div>
                            <div align="center" class="box2">
                                <table align="center" width="100%" border="0">
                                    <tr>
                                        <td align="right" class="label" nowrap="nowrap">Old Password :</td>
                                        <td class="item" width="100%"><input type="password" name="old_passwd" id="user" style="width: 99%;" /></td>
                                    </tr>
                                    <tr>
                                        <td align="right" class="label" nowrap="nowrap">New Password :</td>
                                        <td class="item" width="100%"><input type="password" name="new_passwd" id="user" style="width: 99%;" /></td>
                                    </tr>
                                    <tr>
                                        <td align="right" class="label" nowrap="nowrap">Confirm Password :</td>
                                        <td class="item" width="100%"><input type="password" name="new_passwd2" id="user" style="width: 99%;" /></td>
                                    </tr>
                                </table>
                            </div>
                            <div align="right" class="box2">
                                <button type="button" onclick="window.location.href='/admin'">Cancel</button>
                                <button type="submit">OK</button>
                            </div>
                        
                            <div class="box2 message" id="message" py:if="message">
                                <pre py:content="message"/>
                            </div>
                        </form>
                    </div>
                </td>
            </tr>
        </table>
    </div>
</body>
</html>
