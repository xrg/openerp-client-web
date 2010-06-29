<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>

<%def name="header()">
    <%
        if params.selectable == 1:
            create_url = "/openm2o/edit"
        elif params.selectable == 2:
            create_url = "/openm2m/new"
    %>
    <title>Search ${form.screen.string}</title>

    <script type="text/javascript">
        var form_controller = '/openerp/search';

        function pager_action(action, src) {
            if (src) {
                new ListView(src).go(action);
            } else {
                submit_form(action);
            }
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
    </script>
    % elif params.selectable == 2:
        % if params.get('return_to'):
            <script type="text/javascript">
                function do_select() {
                    var list_this = new ListView('_terp_list');
                    with(window.opener) {
                       var boxes = list_this.getSelectedRecords();
                       if(boxes) {
                            var groups = eval(jQuery('#groups_id').val());
                            var new_groups = new Array();
                            forEach(boxes, function(b){
                                if(jQuery.inArray(parseInt(b), groups) < 0) {
                                    new_groups.push(parseInt(b));
                                }
                            });
                            var color_filters = groups.concat(new_groups);
                            getCalendar(null, null, color_filters);
                       }
                       
                       else {
                            alert(_("No record selected..."));
                            return;
                       }
                    }
                    window.close()
                }
            </script>
        % else:
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
		    </script>
        % endif		    
    % endif
</%def>

<%def name="content()">
<div class="view">
    <form id="search_form" name="search_form" action="" method="post">
        <input type="hidden" id="_terp_source" name="_terp_source" value="${params.source}"/>
        <input type="hidden" id="_terp_selectable" name="_terp_selectable" value="${params.selectable}"/>
        <input type="hidden" id="_terp_search_domain" name="_terp_search_domain" value="${params.search_domain}"/>
        <input type="hidden" id="_terp_filter_domain" name="_terp_filter_domain" value="${params.filter_domain}"/>
        <input type="hidden" id="_terp_search_data" name="_terp_search_data" value="${params.search_data}"/>

        <table width="100%" border="0" cellpadding="2" xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#">
            <tr>
                <td>
                    <table width="100%" class="titlebar" style="border: none;">
                        <tr>
                            <td width="100%">
                                <h1>${_("Search %(name)s", name=form.screen.string)}</h1>
                            </td>
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
        <script type="text/javascript">
            if(jQuery('#${form_name} tr.pagerbar:first td.pager-cell-button')) {
                jQuery('#${form_name} tr.pagerbar:first td.pager-cell-button:first a').click(function() {
                    openLink(openobject.http.getURL('/openerp/openm2m/new', {
                        _terp_model: '${params.model}',
                        _terp_source: '${params.source}',
                        _terp_m2m: '${params.source}',
                        _terp_domain: openobject.dom.get('_terp_domain').value,
                        _terp_context: openobject.dom.get('_terp_context').value}));
                });
            }
        </script>
    </form>
</div>
</%def>
