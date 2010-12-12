<div id="Calendar" class="box-a calendar-a gantt-view">

    <p class="side">
        % if days[0] == days[0].today():
            <a class="button-a disabled" href="javascript: void(0)">${_("Today")}</a>
           % else:
               <a class="button-a" href="javascript: void(0)" title="${_('Today...')}"
                onclick="getCalendar('${days[0].today().isoformat()}', 'day')">${_("Today")}</a>
        % endif
        <a class="button-a prev" href="javascript: void(0)" onclick="getCalendar('${days[0].prev().isoformat()}')">
            <img src="/openerp/static/images/cal_left.png" width="14" height="14" border="0"/>
        </a>
        <a class="button-a next" href="javascript: void(0)" onclick="getCalendar('${days[-1].next().isoformat()}')">
            <img src="/openerp/static/images/cal_right.png" width="14" height="14" border="0"/>
        </a>
        <span class="date-title">${title}</span>
    </p>

    <ul class="head">
        <li class="notab">
        % if mode == 'day':
        <img title="${_('Zoom In')}" height="16" width="16" class="button disabled" src="/openerp/static/images/stock-disabled/gtk-zoom-in.png"/>
        % else:
        <img title="${_('Zoom In')}" height="16" width="16" class="button" src="/openerp/static/images/stock/gtk-zoom-in.png"
            onclick="ganttZoomIn()"/>
        % endif
        </li>
        <li class="notab">
        % if mode == '5years':
        <img title="${_('Zoom Out')}" height="16" width="16" class="button disabled" src="/openerp/static/images/stock-disabled/gtk-zoom-out.png"/>
        % else:
        <img title="${_('Zoom Out')}" height="16" width="16" class="button" src="/openerp/static/images/stock/gtk-zoom-out.png"
            onclick="ganttZoomOut()"/>
        % endif
        </li>
    </ul>

    <table border="0" id="calContainer" width="100%">
    <tr>
        <td id="calMainArea" valign="top">
            <input type="hidden" id="_terp_selected_day" name="_terp_selected_day" value="${selected_day.isoformat()}"/>
            <input type="hidden" id="_terp_selected_mode" name="_terp_selected_mode" value="${mode}"/>
            <input type="hidden" id="_terp_calendar_fields" name="_terp_calendar_fields" value="${calendar_fields}"/>
            <input type="hidden" id="_terp_gantt_level" name="_terp_gantt_level" value="${level}"/>
            % if concurrency_info:
                ${concurrency_info.display()}
            % endif

            <div id="calGantt" class="calGantt" dtFormat="${date_format}" dtStart="${days[0].isoformat()}" dtRange="${len(days)}"><span></span>

                <div id="calHeaderSect">
                    % for count, header in headers:
                    <div class="calTitle" nCount="${count}">${header}</div>
                    % endfor
                    % for header in subheaders:
                    <div class="calSubTitle">${header}</div>
                    % endfor
                </div>

                <div id="calBodySect">
                    % for group in groups:
                    <div class="calGroup"
                        nRecordID="${group['id']}"
                        items="${str(group['items'])}"
                        model="${group['model']}"
                        title="${group['title']}"
                        />
                    % endfor
                    % for evt in events:
                    <div class="calEvent ${evt.classes}"
                        nRecordID="${evt.record_id}"
                        nDaySpan="${evt.dayspan}"
                        dtStart="${str(evt.starts)}"
                        dtEnd="${str(evt.ends)}"
                        title="${evt.title}"
                        nCreationDate="${evt.create_date}"
                        nCreationId="${evt.create_uid}"
                        nWriteDate="${evt.write_date}"
                        nWriteId="${evt.write_uid}"
                        style="background-color: ${evt.color}"/>
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
            window.CAL_INSTANCE = new GanttCalendar();
            window.CAL_INSTANCE.onResize();
        });
    </script>
</div>
