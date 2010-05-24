<%inherit file="/openerp/controllers/templates/base.mako"/>

<%def name="header()">
    <title>${form.screen.string} </title>

    <script type="text/javascript">
        var form_controller = '/openerp/openm2o';
    </script>

    <script type="text/javascript">
        
        function do_select(id, src) {
            viewRecord(id, src);
        }
        
        MochiKit.DOM.addLoadEvent(function(evt) {
        
            var id = parseInt(openobject.dom.get('_terp_id').value) || null;
            var lc = parseInt(openobject.dom.get('_terp_load_counter').value) || 1;

            if (lc > 1 && id) {
                window.opener.document.getElementById('${params.m2o}').value = id;
                window.opener.document.getElementById('${params.m2o}_text').value = '';
                window.opener.setTimeout("signal(openobject.dom.get('${params.m2o}'), 'onchange')", 0);
            }

            if (lc > 1) {
                window.close();
            }
        });
    </script>
</%def>

<%def name="content()">
    <table class="view" cellspacing="5" border="0" width="100%">
        <tr>
            <td>
                <input type="hidden" id="_terp_load_counter" value="${params.load_counter or 0}"/>
                <table width="100%" class="titlebar">
                    <tr>
                        <td width="32px" align="center">
                            <img alt="" src="/openerp/static/images/stock/gtk-edit.png"/>
                        </td>
                        <td width="100%">${form.screen.string}
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td>${form.display()}</td>
        </tr>
        <tr>
            <td>
                <div class="toolbar">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
                        <tr>
                            <td width="100%">
                            </td>
                            <td>
                                <button type="button" onclick="window.close()">${_("Close")}</button>
                                % if form.screen.editable:
                                <button type="button" onclick="submit_form('save')">${_("Save")}</button>
                                % endif
                            </td>
                        </tr>
                    </table>
                </div>
            </td>
        </tr>
    </table>
</%def>
