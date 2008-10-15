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
                    <button type="button" title="Day..." disabled="${tg.selector(mode == 'day')}" onclick="getCalendar(null, 'day')">Day</button>
                    <button type="button" title="Week..." disabled="${tg.selector(mode == 'week')}" onclick="getCalendar(null, 'week')">Week</button>
                    <button type="button" title="Month..." disabled="${tg.selector(mode == 'month')}" onclick="getCalendar(null, 'month')">Month</button>
                </td>
            </tr>
        </table>
        <input type="hidden" id="_terp_selected_day" name="_terp_selected_day" value="${selected_day.isoformat()}"/>
        <input type="hidden" id="_terp_selected_mode" name="_terp_selected_mode" value="${mode}"/>
        <input type="hidden" id="_terp_calendar_fields" name="_terp_calendar_fields" value="${ustr(calendar_fields)}"/>
    </td>
</tr>
<tr>
    <td id="calSidebar" valign="top">
        <div style='border: 1px solid gray; height: 350px; margin-bottom: 4px;'>TODO: tree here</div>
        <div py:replace="groupbox.display()"/>
        <div id="calSearchOptions">
            <table border="0">
                <tr>
                    <td><input type="checkbox" class="checkbox" id="_terp_use_search" name="_terp_use_search" checked="${(use_search or None) and 'checked'}" onclick="getCalendar()"/></td>
                    <td>Apply search filter</td>
                </tr>
            </table>
        </div>
    </td>

    <td id="calMainArea" valign="top">

        <div id="calGantt" class="calGantt" dtFormat="${date_format}" dtStart="${days[0].isoformat()}" dtRange="${len(days)}"><span></span>

            <div id="calHeaderSect">
                <div py:if="len(days) not in (1, 7)" class="calDayName" py:for="day in days">${day.day}</div>
                <div py:if="len(days) in (1, 7)" class="calDayName" py:for="day in days">${ustr(day)}</div>
            </div>

            <div id="calBodySect">
                <div py:for="evt in events" py:strip="">
                    <div class="calEvent" py:if="evt.dayspan > 0"
                         nRecordID="${evt.record_id}"
                         nDaySpan="${evt.dayspan}"
                         dtStart="${str(evt.starts)}"
                         dtEnd="${str(evt.ends)}"
                         title="${evt.description}"
                         style="background-color: ${evt.color}">${evt.title}</div>
                    <div class="calEvent calEventInfo" py:if="evt.dayspan == 0"
                         nRecordID="${evt.record_id}"
                         nDaySpan="${evt.dayspan}"
                         dtStart="${str(evt.starts)}"
                         dtEnd="${str(evt.ends)}"
                         title="${evt.description}"
                         style="color: ${evt.color}">${evt.starts.strftime('%H:%M')} - ${evt.title}</div>
                </div>
            </div>
        </div>

        <script type="text/javascript">
            CAL_INSTANCE = new GanttCalendar();
        </script>

    </td>
</tr>
</table>
