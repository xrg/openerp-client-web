<div id="Calendar" class="box-a calendar-a">
    <p class="side">
        % if day == day.today():
            <a class="button-a" href="javascript: void(0)">${_("Today")}</a>
           % else:
               <a class="button-b" href="javascript: void(0)"
                onclick="getCalendar('${day.today().isoformat()}', 'day')">${_("Today")}</a>
        % endif
    </p>
    <ul class="head">
        <li>
            <a href="javascript: void(0)" title="${_('Month Calendar...')}"
                onclick="getCalendar(null, 'month')">${_("Month")}</a>
        </li>
        <li>
            <a href="javascript: void(0)" title="${_('Week Calendar...')}"
                onclick="getCalendar(null, 'week')">${_("Week")}</a>
        </li>
        <li class="active-tab">
            <a href="javascript: void(0)"
                title="${_('Day Calendar...')}">${_("Day")}</a>
        </li>
    </ul>
    <div class="inner">
        <p class="paging-a">
            <span class="one">
                <a class="first" href="javascript: void(0)"></a>
                <small>|</small>
                <a class="prev" href="javascript: void(0)"
                    onclick="getCalendar('${day.prev().isoformat()}')"></a>
            </span>
            <small>|</small>
            <span class="two">
                <a class="next" href="javascript: void(0)"
                    onclick="getCalendar('${day.next().isoformat()}')"></a>
                <small>|</small>
                <a class="last" href="javascript: void(0)"></a>
            </span>
        </p>
        <h4>
            <span>
                ${day}
            </span>
        </h4>
    </div>
    <table border="0" id="calContainer" width="100%">
        <tr>
            <td id="calMainArea" valign="top">
                <input type="hidden" id="_terp_selected_day"
                    name="_terp_selected_day" value="${day.isoformat()}"/>
                <input type="hidden" id="_terp_selected_mode"
                    name="_terp_selected_mode" value="day"/>
                <input type="hidden" id="_terp_calendar_fields"
                    name="_terp_calendar_fields" value="${calendar_fields}"/>
                % if concurrency_info:
                    ${concurrency_info.display()}
                % endif
                <div id="calWeek" class="calWeek" dtFormat="${date_format}"><span></span>
                    <div id="calHeaderSect">
                        <div dtDay="${day.isoformat()}">${day.name} ${day.day}</div>
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
                                        style="background-color: ${evt.color}" 
                                        class="calEvent allDay">${evt.title}</div>
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
                            style="background-color: ${evt.color}" 
                            class="calEvent noAllDay">
                           <div style="height: 10px;" class="calEventTitle">${evt.starts.strftime('%I:%M %P')} - ${evt.title}</div>
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
