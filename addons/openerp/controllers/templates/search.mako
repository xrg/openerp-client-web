<%inherit file="/openerp/controllers/templates/base.mako"/>

<%def name="header()">
    <title>Search ${form.screen.string}</title>

    <script type="text/javascript">
        var form_controller = '/openerp/search';
    </script>

    <script type="text/javascript">

        function pager_action(action, src){
            if (src)
                new ListView(src).go(action);
           else
                submit_form(action);
        }

    </script>

    % if params.selectable == 1:
    <script type="text/javascript">

        function do_select(res_id){
            if (!res_id) {
                var ids = new ListView('_terp_list').getSelectedRecords();

                if (ids.length<1)
                    return;

                res_id = ids[0];
            }
            
            with (window.opener) {
                
                var value_field = openobject.dom.get('${params.source}');
                var text_field = openobject.dom.get('${params.source}_text');
                
                value_field.value = res_id;
            
                if (text_field){
                    text_field.value = '';
                }

                if (value_field.onchange){
                    value_field.onchange();
                }else{
                    MochiKit.Signal.signal(value_field, 'onchange');
                }
            }
            
            window.close();
        }

        function do_create(){
            act = openobject.http.getURL('/openerp/openm2o/edit', {_terp_model: '${params.model}', 
                                           _terp_source: '${params.source}',
                                           _terp_m2o: '${params.source}',
                                           _terp_domain: openobject.dom.get('_terp_domain').value,
                                           _terp_context: openobject.dom.get('_terp_context').value});
            window.location.href = act;
        }
    </script>
    % elif params.selectable == 2:
    <script type="text/javascript">

        function do_select(id) {

            var source = "${params.source}";
            var list_this = new ListView('_terp_list');

            with(window.opener) {

                var m2m = Many2Many('${params.source}');
                var ids = m2m.getValue();

                if (id){
                    if (findValue(ids, id) == -1) ids.push(id);
                } else {
                    var boxes = list_this.getSelectedItems();

                    if(boxes.length == 0) {
                        alert(_("No record selected..."));
                        return;
                    }

                    forEach(boxes, function(b){
                        if (findValue(ids, b.value) == -1) ids.push(b.value);
                    });
                }

                m2m.setValue(ids);
            }
            window.close();
        }
        
        function do_create(){
            act = openobject.http.getURL('/openerp/openm2m/new', {_terp_model: '${params.model}', 
                                           _terp_source: '${params.source}',
                                           _terp_m2m: '${params.source}',
                                           _terp_domain: openobject.dom.get('_terp_domain').value,
                                           _terp_context: openobject.dom.get('_terp_context').value});
            window.location.href = act;
        }
    </script>
    % endif
</%def>

<%def name="content()">
<div class="view">
    <form id="search_form" name="search_form" action="" method="post" onsubmit="return false;">
        <input type="hidden" id="_terp_source" name="_terp_source" value="${params.source}"/>
        <input type="hidden" id="_terp_selectable" name="_terp_selectable" value="${params.selectable}"/>
        <input type="hidden" id="_terp_search_domain" name="_terp_search_domain" value="${params.search_domain}"/>
        <input type="hidden" id="_terp_filter_domain" name="_terp_filter_domain" value="${params.filter_domain}"/>
        <input type="hidden" id="_terp_search_data" name="_terp_search_data" value="${params.search_data}"/>

        <table width="100%" border="0" cellpadding="2" xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" style="border: none;">
            <tr>
                <td>
                    <table width="100%" class="titlebar" style="border: none;">
                        <tr>
                            <td width="32px" align="center">
                                <img alt="" src="/openerp/static/images/stock/gtk-find.png"/>
                            </td>
                            <td width="100%">${_("Search %(name)s", name=form.screen.string)}</td>
                        </tr>
                    </table>
                </td>
            </tr>
            <tr>
                <td>${form.search.display()}</td>
            </tr>
            <tr>
                <td class="toolbar">
                    <table cellpadding="0" cellspacing="0">
                        <tr>
                            <td width="100%">
                            	<a class="button-a" href="javascript: void(0)" onclick="search_filter()">${_("Filter")}</a>
                            	<a class="button-a" href="javascript: void(0)" onclick="do_create()">${_("New")}</a>
                            	<a class="button-a" href="javascript: void(0)" onclick="do_select()">${_("Select")}</a>
                            	<a class="button-a" href="javascript: void(0)" onclick="window.close()">${_("Close")}</a>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
            <tr>
                <td>${form.screen.display()}</td>
            </tr>
        </table>
    </form>
</div>
</%def>
