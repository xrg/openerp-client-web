<%inherit file="/openerp/controllers/templates/base.mako"/>

<%def name="header()">
    <title>${form.screen.string}</title>

    <script type="text/javascript">
        var form_controller = '/calpopup';
    </script>

    <script type="text/javascript">

        function load_defaults() {
            var pwin = window.opener;
            var elem = pwin.document.getElementById('calEventNew');

            var starts = getNodeAttribute(elem, 'dtStart');
            var ends = getNodeAttribute(elem, 'dtEnd');	
            var params = {
                '_terp_model': openobject.dom.get('_terp_model').value,
                '_terp_fields': pwin.document.getElementById('_terp_calendar_fields').value,
                '_terp_starts' : starts,
                '_terp_ends' : ends,
                '_terp_context': openobject.dom.get('_terp_context').value
            };

            var req = openobject.http.postJSON('/calpopup/get_defaults', params);
            req.addCallback(function(obj){
                forEach(items(obj), function(item){
                    var k = item[0];
                    var v = item[1];

                    var e = openobject.dom.get(k);

                    if (e) e.value = v;
                });
            });
        }

        function on_load() {
            var id = parseInt(openobject.dom.get('_terp_id').value) || 0;
            
            var lc = openobject.dom.get('_terp_load_counter').value;
            lc = parseInt(lc) || 0;

            if (lc > 0) { 
                window.opener.setTimeout('getCalendar()', 0.5);
            }
            
            if (lc > 1) {
                return window.close();
            }

            if (id == 0) {
                load_defaults();
            }
        }

        jQuery(document).ready(on_load);
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
                            <img src="/openerp/static/images/stock/gtk-edit.png"/>
                        </td>
                        <td width="100%">${form.screen.string}</td>
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
