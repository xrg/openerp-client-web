<table border="0" id="calContainer" width="100%" xmlns:py="http://purl.org/kid/ns#">
<tr>
    <td style="width: 200px"><div id="calLoading">Loading...</div></td>
    <td id="calNavigation">
        <table width="100%" class="toolbar">
            <tr>
                <td nowrap="nowrap">
                    <img height="16" width="16" class="button" src="/static/images/stock/gtk-go-back.png" 
                        onclick="getCalendar('${days[0].prev().isoformat()}', null)"/>
                </td>
                <td nowrap="nowrap">
                    <button type="button" title="Today..." 
                        onclick="getCalendar('${days[0].today().isoformat()}', 'day')">Today</button>
                </td>
                <td nowrap="nowrap">
                    <img height="16" width="16" class="button" src="/static/images/stock/gtk-go-forward.png" 
                        onclick="getCalendar('${days[-1].next().isoformat()}', null)"/>
                </td>
                <td nowrap="nowrap" width="100%"><strong>${title}</strong></td>
                <td nowrap="nowrap">
                    <img title="Zoom In" height="16" width="16" src="/static/images/stock-disabled/gtk-zoom-in.png" py:if="mode == 'day'"/>
                    <img title="Zoom In" height="16" width="16" class="button" src="/static/images/stock/gtk-zoom-in.png"  py:if="mode != 'day'"
                        onclick="ganttZoomIn()"/>
                    
                    <img title="Zoom Out" height="16" width="16" src="/static/images/stock-disabled/gtk-zoom-out.png" py:if="mode == 'year'"/>
                    <img title="Zoom Out" height="16" width="16" class="button" src="/static/images/stock/gtk-zoom-out.png" py:if="mode != 'year'"
                        onclick="ganttZoomOut()"/>
                </td>
            </tr>
        </table>
        <input type="hidden" id="_terp_selected_day" name="_terp_selected_day" value="${selected_day.isoformat()}"/>
        <input type="hidden" id="_terp_selected_mode" name="_terp_selected_mode" value="${mode}"/>
        <input type="hidden" id="_terp_calendar_fields" name="_terp_calendar_fields" value="${ustr(calendar_fields)}"/>
    </td>
</tr>
<tr>
    <td id="calSidebarArea" valign="top">
        <div id="calSidebar">
            <div id="calTreeContainer">
                <div id="calTree"/>
            </div>
            <div py:replace="groupbox.display()"/>
            <div id="calSearchOptions">
                <table border="0">
                    <tr>
                        <td>
                            <input type="checkbox" class="checkbox" 
                                id="_terp_use_search" name="_terp_use_search" 
                                checked="${(use_search or None) and 'checked'}" 
                                onclick="getCalendar()"/>
                        </td>
                        <td>Apply search filter</td>
                    </tr>
                </table>
            </div>
        </div>
    </td>

    <td id="calMainArea" valign="top">

        <div id="calGantt" class="calGantt" dtFormat="${date_format}" dtStart="${days[0].isoformat()}" dtRange="${len(days)}"><span></span>

            <div id="calHeaderSect">
                <div class="calDayName" py:for="header in headers">${header}</div>
            </div>

            <div id="calBodySect">
                <div py:for="group in groups" class="calGroup"
                    nRecordID="${group['id']}"
                    items="${str(group['items'])}"
                    model="${group['model']}"
                    title="${group['title']}"/>
                <div py:for="evt in events" class="calEvent"
                    nRecordID="${evt.record_id}"
                    nDaySpan="${evt.dayspan}"
                    dtStart="${str(evt.starts)}"
                    dtEnd="${str(evt.ends)}"
                    title="${evt.title}"
                    style="background-color: ${evt.color}"/>
            </div>
        </div>

        <script type="text/javascript">

            var tree = new TreeGrid('calTree');

            tree.options.showheaders = true;        
            tree.options.expandall = true;

            tree.setHeaders([{"string": "${_('Name')}", "name": "name", "type": "char"}]);
            tree.setRecords('/calendar/gantt_data', {
                "_terp_model": "${model}", 
                "_terp_ids": "${str([e.record_id for e in events])}",
                "_terp_groups": "${str(groups)}"});

            MochiKit.Signal.connect(tree, 'onNodeExpand', onTreeExpand);
            MochiKit.Signal.connect(tree, 'onNodeCollapse', onTreeCollapse);
            MochiKit.Signal.connect(tree, 'onNodeSelect', onTreeSelect);

            tree.render();

            CAL_INSTANCE = new GanttCalendar();
        </script>

    </td>
</tr>
</table>
