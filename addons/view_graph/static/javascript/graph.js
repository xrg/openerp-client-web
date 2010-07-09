var charts = {};
function get_chart(id) {
    return MochiKit.Base.serializeJSON(charts[id]);
}
function setup_charts() {
    jQuery('div.flash-chart').each(function (index, e) {
        var name = jQuery(e).attr('id');
        var chart_id = name.slice(0, -1);

        swfobject.embedSWF(openobject.http.getURL("/view_graph/static/open-flash-chart.swf"), name, 500, 350, "9.0.0",
            "expressInstall.swf", {'get-data': 'get_chart', 'id': chart_id}, {'wmode': 'transparent'});
    });
}
function onChartClick(path) {
	openLink(path)
}

jQuery(document).bind('ready ajaxStop', setup_charts);
