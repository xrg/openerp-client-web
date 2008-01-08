<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="../../templates/master.kid">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Database Admin</title>
    
    <script type="text/javascript">
        function toggle_up(id) {
            if($(id).style.display == 'none') {
                $(id).style.display = '';
            }
            else {
                $(id).style.display = 'none';
            }
        }
        
    </script>    
    
</head>
<body>
    <div class="view" id="dbadmin">
    <br/>
        <div class="box2 welcome">Database Administration</div>
        <div class="box2">
            <div class="toolbar" align="center">
                <button type="button" onclick="toggle_up('dbcreate'); toggle_up('dbadmin');">Create</button>
                <button type="button" onclick="toggle_up('dbdrop'); toggle_up('dbadmin');">Drop</button>
                <button type="button" onclick="toggle_up('dbbackup'); toggle_up('dbadmin');">Backup</button>
                <button type="button" onclick="toggle_up('dbrestore'); toggle_up('dbadmin');">Restore</button>
                <button type="button" onclick="toggle_up('dbpassword'); toggle_up('dbadmin');">Password</button>
            </div>
        </div>
        <div class="box2">
            <table align="center" border="0" width="100%">
                <tr>                            
                    <td align="right">
                        <button type="button" onclick="window.location.href='/admin'">Cancel</button>
                    </td>
                </tr>
            </table>
        </div>
    </div>
 
    <div class="view" id="dbcreate" style="display: None">
        <br/>
        <form action="/dbadmin/createdb" method="post">
            <div class="box2 welcome">Create Database</div>
            <div class="box2" id="create">
                <table align="center" border="0" width="100%">
                    <tr>
                        <td align="right" class="label" nowrap="nowrap">Super admin password :</td>
                        <td class="item" width="100%">
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
                <button type="button" onclick="window.location.href='/dbadmin'">Cancel</button>
                <button type="submit">OK</button>
            </div>

            <div class="box2 message" id="message" py:if="message">
                <pre py:content="message"/>
            </div>
        </form>
    </div>
 
    <div class="view" id="dbdrop" style="display: None">
        <div class="box2 welcome">Drop Database</div>
        <form action="/dbadmin/dropdb" method="post">
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
                <button type="button" onclick="window.location.href='/dbadmin'">Cancel</button>
                <button type="submit">OK</button>
            </div>
        
            <div class="box2 message" id="message" py:if="message">
                <pre py:content="message"/>
            </div>
        </form>
    </div>
    
    <div class="view" id="dbbackup" style="display:None">
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
                            <button type="button" onclick="window.location.href='/dbadmin'">Cancel</button>
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

    <div class="view" id="dbrestore" style="display:None">
        <div class="box2 welcome">Restore Database</div>
        <form action="/dbadmin/restore" method="post" enctype="multipart/form-data">
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
                <button type="button" onclick="window.location.href='/dbadmin'">Cancel</button>
                <button type="submit">OK</button>
            </div>
        
            <div class="box2 message" id="message" py:if="message">
                <pre py:content="message"/>
            </div>
        </form>
    </div>

    <div class="view" id="dbpassword" style="display: None">
        <div class="box2 welcome">Change Password</div>
        <form action="/dbadmin/password" method="post">
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
                <button type="button" onclick="window.location.href='/dbadmin'">Cancel</button>
                <button type="submit">OK</button>
            </div>
        
            <div class="box2 message" id="message" py:if="message">
                <pre py:content="message"/>
            </div>
        </form>
    </div>
</body>
</html>
