<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>

<%def name="header()">
    <title>${form.screen.string} </title>

    <script type="text/javascript">
        var form_controller = '/openerp/openo2m';
    </script>

    <script type="text/javascript">

        function do_select(id, src) {
            viewRecord(id, src);
        }

        jQuery(document).ready(function (){

            var pwin = window.opener;
            var pform = pwin.document.forms['view_form'];

            var form = document.forms['view_form'];
            var fields = [];

            var required_attrs = ['id', 'name', 'value', 'kind', 'class', 'domain', 'context', 'relation'];

            MochiKit.Iter.forEach(pform.elements, function(e){

                if (e.name && e.type != 'button' && e.name.indexOf('${params.o2m}') != 0){

                    var attrs = {};
                    MochiKit.Iter.forEach(required_attrs, function(n){
                        if (e.attributes[n]) attrs[n] = e.attributes[n].value;
                    });
                    attrs['type'] = 'hidden';
                    attrs['disabled'] = 'disabled';
                    attrs['value'] = e.value;

                    var fld = MochiKit.DOM.INPUT(attrs);
                    fields = fields.concat(fld);
                }
            });

            MochiKit.DOM.appendChildNodes(form, fields);

            var lc = openobject.dom.get('_terp_load_counter').value;

            lc = parseInt(lc) || 0;

            if (lc > 0) {
                window.opener.setTimeout("new ListView('${params.o2m}').reload(null, 1)", 0.5);
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
                <input type="hidden" id="_terp_load_counter" value="${params.load_counter}"/>
                <table width="100%" class="titlebar" style="border: none;">
                    <tr>
                        <td width="100%"><h1>${form.screen.string}</h1></td>
                    </tr>
                </table>
            </td>
        </tr>
        
        <tr>
            <td>
                <div class="footer_tool_box">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border: none;">
                        <tr>
                            % if form.screen.editable:
	                            <td class="save_close">
	                            	<a class="button-a" onclick="submit_form('save')" href="javascript: void(0)">${_("Save")}</a>
	                            </td>
                            % endif
                            <td class="save_close">
                            	<a class="button-a" onclick="window.close()" href="javascript: void(0)">${_("Close")}</a>
                            </td>
                            <td width="100%">
                            </td>                            
                        </tr>
                    </table>
                </div>
            </td>
        </tr>
        <tr>
            <td style="padding: 2px 5px 5px;">${form.display()}</td>
        </tr>
    </table>
</%def>
