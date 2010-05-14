<%inherit file="/openerp/controllers/templates/base.mako"/>

<%def name="header()">
    <title>${form.screen.string} </title>

    <script type="text/javascript">
        var form_controller = '/openm2m';
    </script>

    <script type="text/javascript">

        function do_select(id, src) {
            viewRecord(id, src);
        }

        MochiKit.DOM.addLoadEvent(function(evt) {

            var id = parseInt(openobject.dom.get('_terp_id').value) || null;
            var lc = parseInt(openobject.dom.get('_terp_load_counter').value) || 0;

            if (lc > 0 && id) {

                with(window.opener) {

                    var m2m = Many2Many('${params.m2m}');
                    var ids = m2m.getValue();
                    
                    if (MochiKit.Base.findIdentical(ids, id) == -1)
                        ids.push(id);

                    m2m.setValue(ids);
                }
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
                                <button type="button" onclick="submit_form('save')">${_("Save")}</button>
                            </td>
                        </tr>
                    </table>
                </div>
            </td>
        </tr>
    </table>
</%def>
