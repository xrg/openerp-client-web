<table border="0" id="calContainer" width="100%" xmlns:py="http://purl.org/kid/ns#">
<tr>
    <td style="width: 200px"><div id="calLoading">Loading...</div></td>
    <td id="calNavigation">
        <table width="100%" class="toolbar">
            <tr>
                <td nowrap="nowrap"><img height="16" width="16" class="button" src="/static/images/stock/gtk-go-back.png" onclick="getCalendar('/calendar/get/${week.prev()[0].isoformat()}/${week.prev()[-1].isoformat()}')"/></td>
                <td nowrap="nowrap"><button type="button" title="Today..." onclick="getCalendar('/calendar/get/${selected_day.today().isoformat()}')">Today</button></td>
                <td nowrap="nowrap"><img height="16" width="16" class="button" src="/static/images/stock/gtk-go-forward.png" onclick="getCalendar('/calendar/get/${week.next()[0].isoformat()}/${week.next()[-1].isoformat()}')"/></td>
                <td nowrap="nowrap" width="100%"><strong>${ustr(week)}</strong></td>
                <td nowrap="nowrap">
                    <button type="button" title="Day Calendar..." onclick="getCalendar('/calendar/get/${selected_day.isoformat()}')">Day</button>
                    <button type="button" title="Week Calendar..." disabled="disabled">Week</button>
                    <button type="button" title="Month Calendar..." onclick="getCalendar('/calendar/get/${selected_day.year}/${selected_day.month}')">Month</button>
                    <button type="button" title="Gantt view..." onclick="getCalendar('/calendar/gantt/${selected_day.year}/${selected_day.month}')">Gantt</button>
                </td>
            </tr>
        </table>
        <input type="hidden" id="_terp_selected_day" name="_terp_selected_day" value="${selected_day.isoformat()}"/>
        <input type="hidden" id="_terp_calendar_args" name="_terp_calendar_args" value="${week[0].isoformat()}/${week[-1].isoformat()}"/>
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

        <div id="calWeek" class="calWeek" dtFormat="${date_format}"><span></span>

            <div id="calHeaderSect">
                <div py:for="day in week" dtDay="${day.isoformat()}">${day.name} ${day.day}</div>
            </div>

            <div id="calAllDaySect">
                <div py:for="evt in events" py:if="evt.dayspan > 0" nRecordID="${evt.record_id}" nDaySpan="${evt.dayspan}" dtStart="${str(evt.starts)}" dtEnd="${str(evt.ends)}" title="${evt.description}" style="background-color: ${evt.color}" class="calEvent allDay">${evt.title}</div>
            </div>

            <div id="calBodySect">
                <div py:for="evt in events" py:if="evt.dayspan == 0" nRecordID="${evt.record_id}" dtStart="${str(evt.starts)}" dtEnd="${str(evt.ends)}" style="background-color: ${evt.color}" class="calEvent noAllDay">
                   <div style="height: 10px;" class="calEventTitle">${evt.starts.strftime('%I:%M %P')} - ${evt.title}</div>
                   <div class="calEventDesc">${evt.description}</div>
                   <div class="calEventGrip"></div>
                </div>
            </div>

        </div>

        <script type="text/javascript">
            CAL_INSTANCE = new WeekCalendar();
        </script>
    </td>
</tr>
</table>
