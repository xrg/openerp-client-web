<%inherit file="/openerp/controllers/templates/base.mako"/>

<%def name="header()">
    <title>${_("Add Translations")}</title>
    <link href="/openerp/static/css/listgrid.css" rel="stylesheet" type="text/css"/>
    <script type="text/javascript" src="/openerp/static/javascript/listgrid.js"></script>
</%def>

<%def name="content()">
<form action="/translator/save" method="post" enctype="multipart/form-data">
    <input type="hidden" id="_terp_model" name="_terp_model" value="${model}"/>
    <input type="hidden" id="_terp_id" name="_terp_id" value="${id}"/>

    <table class="view" cellspacing="5" border="0" width="100%">
        <tr>
            <td>
                <table width="100%" class="titlebar">
                    <tr>
                        <td width="32px" align="center">
                            <img alt="" src="/openerp/static/images/stock/stock_translate.png"/>
                        </td>
                        <td width="100%">${_("Add Translation")}</td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td>
                <div class="toolbar">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
                        <tr>
                            <td class="label"><label for="translate">${_("Add Translation for:")}</label></td>
                            <td>
                                <select name="translate" id="translate" onchange="window.location.href=openobject.http.getURL('/translator', {_terp_model: '${model}', _terp_id: '${id}', translate: this.value})">
                                    <option value="fields" ${py.selector(translate=='fields')}>${_("Fields")}</option>
                                    <option value="labels" ${py.selector(translate=='labels')}>${_("Labels")}</option>
                                    <option value="relates" ${py.selector(translate=='relates')}>${_("Relates")}</option>
                                    <option value="view" ${py.selector(translate=='view')}>View</option>
                                </select>
                            </td>
                            <td width="100%">&nbsp;</td>
                            <td><button type="submit">${_("Save")}</button></td>
                            <td><button type="button" onclick="window.close()">${_("Close")}</button></td>
                        </tr>
                    </table>
                </div>
            </td>
        </tr>
        % if translate != 'view':
        <tr>
            <td>
                <table class="grid" width="100%" cellpadding="0" cellspacing="0">
                    <tr class="grid-header">
                        % if translate=='fields':
                        <td class="grid-cell" align="right">${_("Field")}</td>
                        % endif
                        % for lang in langs:
                        <td class="grid-cell" width="${100 / len(langs)}%">${lang['name']}</td>
                        % endfor
                    </tr>
                    % for n, v, x, s in data:
                    <tr class="grid-row">
                        % if x:
                        <input type="hidden" name="_terp_models/${n}" value="${x}"/>
                        % endif
                        % if translate=='fields':
                        <td class="grid-cell label" align="right">${s}: </td>
                        % endif
                        % for lang in langs:
                        <td class="grid-cell item">
                            <input type="text" name="${lang['code']}/${n}" value="${v[lang['code']]}" style="width: 100%;"/>
                        </td>
                        % endfor
                    </tr>
                    % endfor
                </table>
            </td>
        </tr>
        % else:
            % for n, data_ in view:
        <tr>
            <td>
                <table width="100%">
                    <tr><td colspan="2"><hr noshade="noshade"/></td></tr>
                    <tr><th colspan="2" align="center">${[l for l in langs if l['code'] == n][0]['name']} (${n})</th></tr>
                    <tr><td colspan="2"><hr noshade="noshade"/></td></tr>
                    % for d in data_:
                    <tr>
                        <td style="width: 50%; text-align: right"><label for="${n}/${d['id']}">${d['src']} = </label></td>
                        <td style="width: 50%">
                            <input type="text" name="${n}/${d['id']}" id="${n}/${d['id']}" value="${d['value']}"
                                   style="width: 100%;"/>
                        </td>
                    </tr>
                    % endfor
                </table>
            </td>
        </tr>
            % endfor
        % endif

        <tr>
            <td>
                <div class="toolbar">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
                        <tr>
                            <td width="100%">&nbsp;</td>
                            <td><button type="submit">${_("Save")}</button></td>
                            <td><button type="button" onclick="window.close()">${_("Close")}</button></td>
                        </tr>
                    </table>
                </div>
            </td>
        </tr>
    </table>
</form>
</%def>
