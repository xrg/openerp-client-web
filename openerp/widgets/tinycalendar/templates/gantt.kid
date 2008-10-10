<table border="0" id="calContainer" width="100%" xmlns:py="http://purl.org/kid/ns#">
<tr>
    <td style="width: 200px"><div id="calLoading">Loading...</div></td>
    <td id="calNavigation">
        <table width="100%" class="toolbar">
            <tr>
                <td nowrap="nowrap"><img height="16" width="16" class="button" src="/static/images/stock/gtk-go-back.png" onclick="alert('TODO: prev span')"/></td>
                <td nowrap="nowrap"><button type="button" title="Today..." onclick="alert('TODO: goto the current date')">Today</button></td>
                <td nowrap="nowrap"><img height="16" width="16" class="button" src="/static/images/stock/gtk-go-forward.png" onclick="alert('TODO: next span')"/></td>
                <td nowrap="nowrap" width="100%"><strong>${ustr(month[0])} - ${ustr(month[-1])}</strong></td>
                <td nowrap="nowrap">
                    <img height="16" width="16" class="button" src="/static/images/stock/gtk-zoom-in.png" onclick="alert('TODO: reduce time/date period')"/>
                    <img height="16" width="16" class="button" src="/static/images/stock/gtk-zoom-out.png" onclick="alert('TODO: increse time/date period')"/>
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
        <div style='border: 1px solid gray; height: 350px;'>TODO: tree here</div>
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
                <div class="calDayName" py:for="day in month">${day.day}</div>
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
