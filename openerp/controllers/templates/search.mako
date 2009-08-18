<%inherit file="master.mako"/>
<%! show_header_footer=False %>
<%def name="header()">
    <title>Search ${form.screen.string}</title>

    <script type="text/javascript">
        var form_controller = '/search';
    </script>

    <script type="text/javascript">

        function submit_search_form(action){
            form = $('search_form');
            setNodeAttribute(form, 'action', action);

            disable_hidden_search_fields();

            form.submit();
        }

        function pager_action(action, src){
            if (src)
                new ListView(src).go(action);
           else
                submit_search_form(action);
        }

        function disable_hidden_search_fields(){
            // disable fields of hidden tab

            var hidden_tab = getElementsByTagAndClassName('div', 'tabbertabhide', 'search_form')[0];
            var disabled = [];

            disabled = disabled.concat(getElementsByTagAndClassName('input', null, hidden_tab));
            disabled = disabled.concat(getElementsByTagAndClassName('textarea', null, hidden_tab));
            disabled = disabled.concat(getElementsByTagAndClassName('select', null, hidden_tab));

            forEach(disabled, function(fld){
                fld.disabled = true;
            });

            return true;
        }

    </script>

    % if params.selectable == 1:
    <script type="text/javascript">

        function do_select(id){
            if (!id) {
                var ids = new ListView('_terp_list').getSelectedRecords();

                if (ids.length<1)
                    return;

                id = ids[0];
            }
            
            with (window.opener) {
                
                var value_field = getElement('${params.source}');
                var text_field = getElement('${params.source}_text');
                
                value_field.value = id;
            
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
            act = getURL('/openm2o/edit', {_terp_model: '${params.model}', 
                                           _terp_source: '${params.source}',
                                           _terp_m2o: '${params.source}',
                                           _terp_domain: $('_terp_domain').value,
                                           _terp_context: $('_terp_context').value});
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
            act = getURL('/openm2m/new', {_terp_model: '${params.model}', 
                                           _terp_source: '${params.source}',
                                           _terp_m2m: '${params.source}',
                                           _terp_domain: $('_terp_domain').value,
                                           _terp_context: $('_terp_context').value});
            window.location.href = act;
        }
    </script>
    % endif
</%def>

<%def name="content()">
<div class="view">
    <form id="search_form" name="search_form" action="/search/find" method="post" onsubmit="return disable_hidden_search_fields();">
        <input type="hidden" id="_terp_source" name="_terp_source" value="${params.source}"/>
        <input type="hidden" id="_terp_selectable" name="_terp_selectable" value="${params.selectable}"/>
        <input type="hidden" id="_terp_search_domain" name="_terp_search_domain" value="${params.search_domain}"/>
        <input type="hidden" id="_terp_search_data" name="_terp_search_data" value="${params.search_data}"/>

        <table width="100%" border="0" cellpadding="2" xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#">
            <tr>
                <td>
                    <table width="100%" class="titlebar">
                        <tr>
                            <td width="32px" align="center">
                                <img src="/static/images/stock/gtk-find.png"/>
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
                                <button type="submit">${_("Filter")}</button>
                                <button type="button" onclick="do_create()">${_("New")}</button>
                                <button type="button" onclick="do_select()">${_("Select")}</button>
                            </td>
                            <td>
                                <button type="button" onclick="window.close()">${_("Close")}</button>
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
