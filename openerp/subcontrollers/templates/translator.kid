<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="../../templates/master.kid">
<head>
    <title>Add Translations</title>
    <link href="/static/css/listgrid.css" rel="stylesheet" type="text/css"/>
    <script type="text/javascript" src="/static/javascript/listgrid.js"></script>
</head>
<body>

<form action="/translator/save" method="post" enctype="multipart/form-data">
    <input type="hidden" id="_terp_model" name="_terp_model" value="${model}"/>
    <input type="hidden" id="_terp_id" name="_terp_id" value="${id}"/>

    <table class="view" cellspacing="5" border="0" width="100%">
        <tr>
            <td>
                <table width="100%" class="titlebar">
                    <tr>
                        <td width="32px" align="center">
                            <img src="/static/images/stock/stock_translate.png"/>
                        </td>
                        <td width="100%">Add Translation</td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td>
                <div class="toolbar">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
                        <tr>
                            <td class="label">Add Translation for: </td>
                            <td>
                                <select name="translate" onchange="window.location.href=getURL('/translator', {_terp_model: '$model', _terp_id: '$id', translate: this.value})">
                                    <option value="fields" selected="${tg.selector(translate=='fields')}">Fields</option>
                                    <option value="labels" selected="${tg.selector(translate=='labels')}">Labels</option>
                                    <option value="relates" selected="${tg.selector(translate=='relates')}">Relates</option>
                                    <option value="view" selected="${tg.selector(translate=='view')}">View</option>
                                </select>
                            </td>
                            <td width="100%">&nbsp;</td>
                            <td><button type="submit">Save</button></td>
                            <td><button type="button" onclick="window.close()">Close</button></td>
                        </tr>
                    </table>
                </div>
            </td>
        </tr>
        <tr py:if="translate != 'view'">
            <td>
                <table class="grid" width="100%" cellpadding="0" cellspacing="0">
                    <tr class="grid-header">
                        <td py:if="translate=='fields'" class="grid-cell" align="right">Field</td>
                        <td py:for="lang in langs" class="grid-cell" py:content="lang['name']" width="${100 / len(langs)}%">Language</td>
                    </tr>
                    <tr class="grid-row" py:for="n, v, x, s in data">
                        <input type="hidden" name="_terp_models/${n}" value="${x}" py:if="x"/>
                        <td py:if="translate=='fields'" class="grid-cell label" align="right">${s}: </td>
                        <td class="grid-cell item" py:for="lang in langs">
                            <input type="text" name="${lang['code']}/${n}" value="${v[lang['code']]}" style="width: 100%;"/>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>

        <tr py:if="translate == 'view'" py:for="n, data in view">
            <td>
                <table width="100%">
                    <tr><td colspan="2"><hr noshade="noshade"/></td></tr>
                    <tr><th colspan="2" align="center">${[l for l in langs if l['code'] == n][0]['name']} (${n})</th></tr>
                    <tr><td colspan="2"><hr noshade="noshade"/></td></tr>
                    <tr py:for="d in data">
                        <td style="width: 50%; text-align: right">${d['src']} = </td>
                        <td style="width: 50%">
                            <input type="text" name="${n}/${d['id']}" value="${d['value']}" style="width: 100%;"/>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>

        <tr>
            <td>
                <div class="toolbar">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
                        <tr>
                            <td width="100%">&nbsp;</td>
                            <td><button type="submit">Save</button></td>
                            <td><button type="button" onclick="window.close()">Close</button></td>
                        </tr>
                    </table>
                </div>
            </td>
        </tr>
    </table>
</form>

</body>
</html>
