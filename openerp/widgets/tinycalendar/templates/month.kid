<table border="0" id="calContainer" width="100%" xmlns:py="http://purl.org/kid/ns#">
<tr>
    <td style="width: 200px"><div id="calLoading">Loading...</div></td>
    <td id="calNavigation">
        <table width="100%" class="toolbar">
            <tr>
                <td nowrap="nowrap"><img height="16" width="16" class="button" src="/static/images/stock/gtk-go-back.png" onclick="getCalendar('${month.prev().year}-${month.prev().month}-01')"/></td>
                <td nowrap="nowrap"><button type="button" title="${_('Today...')}" onclick="getCalendar('${selected_day.today().isoformat()}', 'day')">Today</button></td>
                <td nowrap="nowrap"><img height="16" width="16" class="button" src="/static/images/stock/gtk-go-forward.png" onclick="getCalendar('${month.next().year}-${month.next().month}-01')"/></td>
                <td nowrap="nowrap" width="100%"><strong>${ustr(month)}</strong></td>
                <td nowrap="nowrap">
                    <button type="button" title="${_('Day Calendar...')}" onclick="getCalendar(null, 'day')">Day</button>
                    <button type="button" title="${_('Week Calendar...')}" onclick="getCalendar(null, 'week')">Week</button>
                    <button type="button" title="${_('Month Calendar...')}" disabled="disabled">Month</button>
                </td>
            </tr>
        </table>
        <input type="hidden" id="_terp_selected_day" name="_terp_selected_day" value="${selected_day.isoformat()}"/>
        <input type="hidden" id="_terp_selected_mode" name="_terp_selected_mode" value="month"/>
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
                    <td><input type="checkbox" class="checkbox" id="_terp_use_search" name="_terp_use_search" checked="${(use_search or None) and 'checked'}" onclick="getCalendar()"/></td>
                    <td>Apply search filter</td>
                </tr>
            </table>
        </div>
    </td>

    <td id="calMainArea" valign="top">

        <div id="calMonth" class="calMonth" dtFormat="${date_format}" dtStart="${month[0].isoformat()}" dtFirst="${month.year}-${month.month}-01"><span></span>

            <div id="calHeaderSect">
                <div class="calDayName" py:for="day in month.weeks[0]">${day.name}</div>
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
            CAL_INSTANCE = new MonthCalendar();
        </script>

    </td>
</tr>
</table>
