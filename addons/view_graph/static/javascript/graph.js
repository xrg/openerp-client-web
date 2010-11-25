var charts = {};
function get_chart(id) {
    return MochiKit.Base.serializeJSON(charts[id]);
}
function setup_charts() {
	var last_chart = jQuery('div.flash-chart').get().length;

	jQuery('div.flash-chart').each(function (index, e) {
		var name = jQuery(e).attr('id');
		var chart_id = name.slice(0, -1);
		swfobject.embedSWF(openobject.http.getURL("/view_graph/static/open-flash-chart.swf"), name, '100%', 350, "9.0.0",
			"expressInstall.swf", {'get-data': 'get_chart', 'id': chart_id}, {'wmode': 'transparent'});
	});
	
}
function reload_graph(clear) {
    this.name = '_terp_list';
    var args = {};
    var names = ('/' + this.name).split('/');

    var prefix = '';
    var items = openobject.dom.select('input');

    while (names.length) {

        var name = names.shift();
        prefix = prefix + (name ? name + '/' : '');

        var pattern = prefix + '_terp_';

        forEach(items, function(item) {
            if (item.name.match("^" + pattern) == pattern && !item.name.match(/^_terp_listfields\//)) {
                args[item.name] = item.value;
            }
        });
    }
    var _terp_search_domain = openobject.dom.get('_terp_search_domain').value;
    if(clear) {
        _terp_search_domain = '[]'
    }
    args = jQuery.extend(args, {
            _terp_source: this.name,
            _terp_editable: openobject.dom.get('_terp_editable').value,
            _terp_group_by_ctx: openobject.dom.get('_terp_group_by_ctx').value,
            _terp_search_domain: _terp_search_domain,
            _terp_search_data: openobject.dom.get('_terp_search_data').value,
            _terp_filter_domain: openobject.dom.get('_terp_filter_domain').value
	});
    jQuery.ajax({
        url: '/openerp/listgrid/reload_graph',
        dataType: 'json',
        data: args,
        type: 'POST',
        success: function(obj) {
            jQuery('div.graph-block').replaceWith(obj.view);
            return;
        }
    });
}
function onChartClick(path) {
	openLink(path)
}

jQuery(document).bind('ready ajaxStop', setup_charts);
