<div id="Calendar" class="box-a calendar-a month-view">
    <p class="side">
        <a class="button-a" href="javascript:void(0)" title="${_('Today...')}" 
            onclick="getCalendar('${selected_day.today().isoformat()}', 'day')">${_("Today")}</a>
        <a class="button-a prev" href="javascript: void(0)" onclick="getCalendar('${month.prev().year}-${month.prev().month}-01')">
            <img src="/openerp/static/images/cal_left.png" width="14" height="14" border="0"/>
        </a>
        <a class="button-a next" href="javascript: void(0)" onclick="getCalendar('${month.next().year}-${month.next().month}-01')">
            <img src="/openerp/static/images/cal_right.png" width="14" height="14" border="0"/>
        </a>
        <span class="date-title">${month}</span>
    </p>
    <ul class="head">
        <li class="active-tab">
            <a href="javascript: void(0)" title="${_('Month Calendar...')}">${_("Month")}</a>
        </li>
        <li>
            <a href="javascript: void(0)" title="${_('Week Calendar...')}" 
                onclick="getCalendar(null, 'week')">${_("Week")}</a>
        </li>
        <li>
            <a href="javascript: void(0)" title="${_('Day Calendar...')}" 
                onclick="getCalendar(null, 'day')">${_("Day")}</a>
        </li>
    </ul>
    <table border="0" id="calContainer" width="100%">
        <tr>
            <td id="calMainArea" valign="top" width="100%" style="width: 100%">
                <input type="hidden" id="_terp_selected_day" 
                    name="_terp_selected_day" value="${selected_day.isoformat()}"/>
                <input type="hidden" id="_terp_selected_mode" 
                    name="_terp_selected_mode" value="month"/>
                <input type="hidden" id="_terp_calendar_fields" 
                    name="_terp_calendar_fields" value="${calendar_fields}"/>
                % if concurrency_info:
                    ${concurrency_info.display()}
                % endif
                <div id="calMonth" class="calMonth" 
                    dtFormat="${date_format}" 
                    dtStart="${month[0].isoformat()}" 
                    dtFirst="${month.year}-${month.month}-01"><span></span>
                    <div id="calHeaderSect">
                    % for day in month.weeks[0]:
                        <div class="calDayName">${day.name}</div>
                    % endfor
                    </div>
                    <div id="calBodySect">
                        % for evt in events:
                            % if evt.dayspan > 0:
                                <div class="calEvent ${evt.classes}"
                                    nRecordID="${evt.record_id}"
                                    nDaySpan="${evt.dayspan}"
                                    dtStart="${str(evt.starts)}"
                                    dtEnd="${str(evt.ends)}"
                                    title="${evt.description}"
                                    nCreationDate="${evt.create_date}"
                                    nCreationId="${evt.create_uid}"
                                    nWriteDate="${evt.write_date}"
                                    nWriteId="${evt.write_uid}"
                                    style="background-color: ${evt.color}">${evt.title}</div>
                            % endif
                            % if evt.dayspan == 0:
                                <div class="calEvent calEventInfo ${evt.classes}"
                                    nRecordID="${evt.record_id}"
                                    nDaySpan="${evt.dayspan}"
                                    dtStart="${str(evt.starts)}"
                                    dtEnd="${str(evt.ends)}"
                                    title="${evt.description}"
                                    nCreationDate="${evt.create_date}"
                                    nCreationId="${evt.create_uid}"
                                    nWriteDate="${evt.write_date}"
                                    nWriteId="${evt.write_uid}"
                                    style="color: ${evt.color}">${evt.starts.strftime('%H:%M')} - ${evt.title}</div>
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
            window.CAL_INSTANCE = null;
        }
        jQuery(function(){
            window.CAL_INSTANCE = new MonthCalendar();
            window.CAL_INSTANCE.onResize();
        });
    </script>
</div>
