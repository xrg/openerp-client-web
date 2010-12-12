<div id="Calendar" class="box-a calendar-a week-view">
    <p class="side">
        <a class="button-a" href="javascript:void(0)" title="${_('Today...')}" 
            onclick="getCalendar('${selected_day.today().isoformat()}', 'day')">${_("Today")}</a>
        <a class="button-a prev" href="javascript: void(0)" onclick="getCalendar('${week.prev()[0].isoformat()}')">
            <img src="/openerp/static/images/cal_left.png" width="14" height="14" border="0"/>
        </a>
        <a class="button-a next" href="javascript: void(0)" onclick="getCalendar('${week.next()[0].isoformat()}')">
            <img src="/openerp/static/images/cal_right.png" width="14" height="14" border="0"/>
        </a>
        <span class="date-title">
            ${week}
            <small>(${_('Week %(number)s', number=week.number)})</small>
        </span>
    </p>
    <ul class="head">
        <li>
            <a href="javascript: void(0)" title="${_('Month Calendar...')}" 
                onclick="getCalendar(null, 'month')">${_("Month")}</a>
        </li>
        <li class="active-tab">
            <a href="javascript: void(0)" title="${_('Week Calendar...')}">${_("Week")}</a>
        </li>
        <li>
            <a href="javascript: void(0)" title="${_('Day Calendar...')}" 
                onclick="getCalendar(null, 'day')">${_("Day")}</a>
        </li>
    </ul>
    <table border="0" id="calContainer" width="100%">
        <tr>
            <td id="calMainArea" valign="top">
                <input type="hidden" id="_terp_selected_day"
                    name="_terp_selected_day" value="${selected_day.isoformat()}"/>
                <input type="hidden" id="_terp_selected_mode"
                    name="_terp_selected_mode" value="week"/>
                <input type="hidden" id="_terp_calendar_fields"
                    name="_terp_calendar_fields" value="${calendar_fields}"/>
                % if concurrency_info:
                    ${concurrency_info.display()}
                % endif
                <div id="calWeek" class="calWeek" dtFormat="${date_format}"><span></span>
                    <div id="calHeaderSect">
                        % for day in week:
                        <div dtDay="${day.isoformat()}">${day.name} ${day.day}</div>
                        % endfor
                    </div>
                    <div id="calAllDaySect">
                        % for evt in events:
                            % if evt.dayspan > 0:
                                <div nRecordID="${evt.record_id}"
                                    nDaySpan="${evt.dayspan}"
                                    dtStart="${str(evt.starts)}"
                                    dtEnd="${str(evt.ends)}"
                                    title="${evt.description}"
                                    nCreationDate="${evt.create_date}"
                                    nCreationId="${evt.create_uid}"
                                    nWriteDate="${evt.write_date}"
                                    nWriteId="${evt.write_uid}"
                                    style="background-color: ${evt.color};"
                                    class="calEvent allDay ${evt.classes}">${evt.title}</div>
                            % endif
                        % endfor
                    </div>
                    <div id="calBodySect">
                        % for evt in events:
                            % if evt.dayspan == 0:
                        <div nRecordID="${evt.record_id}"
                            dtStart="${str(evt.starts)}"
                            dtEnd="${str(evt.ends)}"
                            nCreationDate="${evt.create_date}"
                            nCreationId="${evt.create_uid}"
                            nWriteDate="${evt.write_date}"
                            nWriteId="${evt.write_uid}"
                            style="background-color: ${evt.color};"
                            class="calEvent noAllDay ${evt.classes}">
                           <div style="height: 10px;" class="calEventTitle">${evt.starts.strftime('%H:%M')} - ${evt.title}</div>
                           <div class="calEventDesc">${evt.description}</div>
                           <div class="calEventGrip"></div>
                        </div>
                            % endif
                        % endfor
                    </div>
                </div>
            </td>
        </tr>
    </table>
    <script type="text/javascript">
        if (window.CAL_INSTANCE) {
            window.CAL_INSTANCE.__delete__();
        }
        jQuery(function(){
            window.CAL_INSTANCE = new WeekCalendar();
            window.CAL_INSTANCE.onResize();
        });
    </script>
</div>
