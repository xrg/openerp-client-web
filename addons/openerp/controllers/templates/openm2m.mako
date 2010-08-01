<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>

<%def name="header()">
    <title>${form.screen.string} </title>

    <script type="text/javascript">
        var form_controller = '/openerp/openm2m';
    </script>

    <script type="text/javascript">

        function do_select(id, src) {
            viewRecord(id, src);
        }

        jQuery(document).ready(function() {

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
    <table class="view" cellspacing="5" border="0" width="100%" style="border: none;">
        <tr>
            <td>
                <input type="hidden" id="_terp_load_counter" value="${params.load_counter or 0}"/>
                <table width="100%" class="titlebar" style="border: none;">
                    <tr>
                        <td width="100%"><h1>${form.screen.string}</h1></td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td>${form.display()}</td>
        </tr>
        <tr>
            <td style="padding-top: 0px;">
                <div class="toolbar footer_tool_box">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border: none;">
                        <tr>
                            <td width="100%">
                            </td>
                            <td>
                            	<a class="button-a" href="javascript: void(0)" onclick="window.close()">${_("Close")}</a>
                            </td>
                            <td>
                            	<a class="button-a" href="javascript: void(0)" onclick="submit_form('save')">${_("Save")}</a>
                            </td>
                        </tr>
                    </table>
                </div>
            </td>
        </tr>
    </table>
</%def>
