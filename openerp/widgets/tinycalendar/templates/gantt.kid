<table border="0" id="calContainer" width="100%" xmlns:py="http://purl.org/kid/ns#">
<tr>
    <td style="width: 200px"><div id="calLoading">Loading...</div></td>
    <td id="calNavigation">
        <table width="100%" class="toolbar">
            <tr>
                <td nowrap="nowrap"><img height="16" width="16" class="button" src="/static/images/stock/gtk-go-back.png" onclick="getCalendar('/calendar/gantt/${month.prev().year}/${month.prev().month}')"/></td>
                <td nowrap="nowrap"><button type="button" title="Today..." onclick="getCalendar('/calendar/get/${selected_day.today().isoformat()}')">Today</button></td>
                <td nowrap="nowrap"><img height="16" width="16" class="button" src="/static/images/stock/gtk-go-forward.png" onclick="getCalendar('/calendar/gantt/${month.next().year}/${month.next().month}')"/></td>
                <td nowrap="nowrap" width="100%"><strong>${ustr(month)}</strong></td>
                <td nowrap="nowrap">
                    <button type="button" title="Day Calendar..." onclick="getCalendar('/calendar/get/${selected_day.isoformat()}')">Day</button>
                    <button type="button" title="Week Calendar..." onclick="getCalendar('/calendar/get/${selected_day.week[0].isoformat()}/${selected_day.week[-1].isoformat()}')">Week</button>
                    <button type="button" title="Month Calendar..." onclick="getCalendar('/calendar/get/${selected_day.year}/${selected_day.month}')">Month</button>
                    <button type="button" title="Gantt view..." disabled="disabled">Gantt</button>
                </td>
            </tr>
        </table>
        <input type="hidden" id="_terp_selected_day" name="_terp_selected_day" value="${selected_day.isoformat()}"/>
        <input type="hidden" id="_terp_calendar_args" name="_terp_calendar_args" value="${month.year}/${month.month}"/>
        <input type="hidden" id="_terp_calendar_fields" name="_terp_calendar_fields" value="${ustr(calendar_fields)}"/>
    </td>
</tr>
<tr>
    <td id="calSidebar" valign="top">
        <div py:replace="minical.display()"/>
        <div py:replace="groupbox.display()"/>
        <div id="calSearchOptions">
            <table border="0">
                <tr>
                    <td><input type="checkbox" class="checkbox" id="_terp_use_search" name="_terp_use_search" checked="${(use_search or None) and 'checked'}" onclick="getCalendar('${groupbox.action}')"/></td>
                    <td>Apply search filter</td>
                </tr>
            </table>
        </div>
    </td>

    <td id="calMainArea" valign="top">

        <div id="calGantt" class="calGantt" dtFormat="${date_format}" dtStart="${month[0].isoformat()}" dtFirst="${month.year}-${month.month}-01"><span></span>

            <div id="calHeaderSect">
                <div class="calDayName" py:for="week in month.weeks">${week[0].strftime('Week %W, %Y')}</div>
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
