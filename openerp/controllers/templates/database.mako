<%inherit file="master.mako"/>

<%def name="header()">
    <title>${form.string}</title>

    <script type="text/javascript" src="/static/javascript/waitbox.js"></script>
    <link rel="stylesheet" type="text/css" href="/static/css/waitbox.css"/>

    <style type="text/css">
        form table {
            margin-top: 20px;
            padding: 5px;
            border: 4px double #c0c0c0;
        }

        form th {
            padding: 0 4px;
            text-align: right;
            white-space: nowrap;
            font-weight: normal;
        }

        form select {
            min-width: 100px;
        }

        .submitbutton td {
            text-align: right;
        }

        .submitbutton {
            border: solid 1px #888888;
            background: url(/static/images/button_bg.png) repeat-x left top;
            color: #000;
            padding: 0px 2px;
            font-size: 11px;
            white-space: nowrap;
            min-width: 80px;
        }
        
        td.labelcol {
            text-align: right;
        }

        .submitbutton:hover {
            background: url(/static/images/button_bg2.png) repeat-x left top;
        }

        .fieldcol .requiredfield {
            background-color: #CCD9FF;
        }

        .fielderror {
            color: red;
        }

    </style>

    <script type="text/javascript">

        var WAITBOX = null;

        MochiKit.DOM.addLoadEvent(function(evt){
            WAITBOX = new WaitBox();
        });

        var dbView = function(name) {
            window.location.href = '/database/' + name;
        }

        var on_create = function() {
            MochiKit.Async.callLater(2, function(){
                WAITBOX.show();
            });
            return true;
        }

    </script>
</%def>

<%def name="content()">
    <table class="view" cellpadding="0" cellspacing="0" border="0" width="100%">
        <tr>
            <td valign="top">
                <table width="100%" class="titlebar">
                    <tr>
                        <td width="32px" align="center">
                            <img src="/static/images/stock/stock_person.png"/>
                        </td>
                        <td width="100%">${form.string}</td>
                        <td nowrap="nowrap">
                            <button type="button" 
                                title="${_('Create new database')}"
                                ${py.disabled(form.name=='create')}
                                onclick="dbView('create')">${_("Create")}</button>
                            <button type="button" 
                                title="${_('Drop database')}"
                                ${py.disabled(form.name=='drop')}
                                onclick="dbView('drop')">${_("Drop")}</button>
                            <button type="button" 
                                title="${_('Backup database')}"
                                ${py.disabled(form.name=='backup')}
                                onclick="dbView('backup')">${_("Backup")}</button>
                            <button type="button" 
                                title="${_('Restore database')}"
                                ${py.disabled(form.name=='restore')}
                                onclick="dbView('restore')">${_("Restore")}</button>
                            <button type="button" 
                                title="${_('Change Administrator Password')}"
                                ${py.disabled(form.name=='password')}
                                onclick="dbView('password')">${_("Password")}</button>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td valign="top" align="center">${form.display()}</td>
        </tr>
    </table>
</%def>
