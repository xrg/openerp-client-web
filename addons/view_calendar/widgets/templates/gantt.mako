<div id="Calendar" class="box-a calendar-a">

    <p class="side">
        <a class="button-a" href="javascript: void(0)" title="${_('Today...')}"
            onclick="getCalendar('${days[0].today().isoformat()}', 'day')">${_("Today")}</a>
    </p>

    <ul class="head">
        <li>
        % if mode == 'day':
        <img title="${_('Zoom In')}" height="16" width="16" src="/openerp/static/images/stock-disabled/gtk-zoom-in.png"/>
        % else:
        <img title="${_('Zoom In')}" height="16" width="16" class="button" src="/openerp/static/images/stock/gtk-zoom-in.png"
            onclick="ganttZoomIn()"/>
        % endif
        </li>
        <li>
        % if mode == '5years':
        <img title="${_('Zoom Out')}" height="16" width="16" src="/openerp/static/images/stock-disabled/gtk-zoom-out.png"/>
        % else:
        <img title="${_('Zoom Out')}" height="16" width="16" class="button" src="/openerp/static/images/stock/gtk-zoom-out.png"
            onclick="ganttZoomOut()"/>
        % endif
        </li>
    </ul>

    <div class="inner">
        <p class="paging-a">
            <span class="one">
                <a class="first" href="javascript: void(0)"></a>
                <small>|</small>
                <a class="prev" href="javascript: void(0)" 
                    onclick="getCalendar('${days[0].prev().isoformat()}', null)"></a>
            </span>
            <small>|</small>
            <span class="two">
                <a class="next" href="javascript: void(0)" 
                    onclick="getCalendar('${days[-1].next().isoformat()}', null)"></a>
                <small>|</small>
                <a class="last" href="javascript: void(0)"></a>
            </span>
        </p>
        <h4>
            <span>${title}</span>
        </h4>
    </div>

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
                <div class="calEvent"
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
        CAL_INSTANCE = new GanttCalendar();
    </script>
</div>
