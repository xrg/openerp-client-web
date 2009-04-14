<table border="0" id="calContainer" width="100%">
<tr>
    <td style="width: 200px"><div id="calLoading">Loading...</div></td>
    <td id="calNavigation">
        <table width="100%" class="toolbar">
            <tr>
                <td nowrap="nowrap"><img height="16" width="16" class="button" src="/static/images/stock/gtk-go-back.png" onclick="getCalendar('${day.prev().isoformat()}')"/></td>
                <td nowrap="nowrap"><button type="button" title="${_('Today...')}" ${py.selector("disabled",day == day.today())} onclick="getCalendar('${day.today().isoformat()}', 'day')">Today</button></td>
                <td nowrap="nowrap"><img height="16" width="16" class="button" src="/static/images/stock/gtk-go-forward.png" onclick="getCalendar('${day.next().isoformat()}')"/></td>
                <td nowrap="nowrap" width="100%"><strong>${ustr(day)}</strong></td>
                <td nowrap="nowrap">
                    <button type="button" title="${_('Day Calendar...')}" disabled="disabled">Day</button>
                    <button type="button" title="${_('Week Calendar...')}" onclick="getCalendar(null, 'week')">Week</button>
                    <button type="button" title="${_('Month Calendar...')}" onclick="getCalendar(null, 'month')">Month</button>
                </td>
            </tr>
        </table>
        <input type="hidden" id="_terp_selected_day" name="_terp_selected_day" value="${day.isoformat()}"/>
        <input type="hidden" id="_terp_selected_mode" name="_terp_selected_mode" value="day"/>
        <input type="hidden" id="_terp_calendar_fields" name="_terp_calendar_fields" value="${ustr(calendar_fields)}"/>
        % if concurrency_info:
            ${concurrency_info.display()}
        % endif
    </td>
</tr>
<tr>
    <td id="calSidebar" valign="top">
        ${minical.display()}
        ${groupbox.display()}
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

        <div id="calWeek" class="calWeek" dtFormat="${date_format}"><span></span>

            <div id="calHeaderSect">
                <div dtDay="${day.isoformat()}">${day.name} ${day.day}</div>
            </div>

            <div id="calAllDaySect">
                % for evt in events:
                    % if evt.dayspan > 0:
                <div nRecordID="${evt.record_id}" nDaySpan="${evt.dayspan}" dtStart="${str(evt.starts)}" dtEnd="${str(evt.ends)}" title="${evt.description}" style="background-color: ${evt.color}" class="calEvent allDay">${evt.title}</div>
                    % endif
                % endfor
            </div>

            <div id="calBodySect">
                % for evt in events:
                    % if evt.dayspan == 0:
                <div nRecordID="${evt.record_id}" dtStart="${str(evt.starts)}" dtEnd="${str(evt.ends)}" style="background-color: ${evt.color}" class="calEvent noAllDay">
                   <div style="height: 10px;" class="calEventTitle">${evt.starts.strftime('%I:%M %P')} - ${evt.title}</div>
                   <div class="calEventDesc">${evt.description}</div>
                   <div class="calEventGrip"></div>
                </div>
                    % endif
                % endfor
            </div>

        </div>

        <script type="text/javascript">
            CAL_INSTANCE = new WeekCalendar();
        </script>
    </td>
</tr>
</table>

