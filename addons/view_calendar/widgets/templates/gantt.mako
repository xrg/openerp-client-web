<table border="0" id="calContainer" width="100%">
<tr>
    <td width="100%" id="calNavigation">
        <table width="100%" class="toolbar">
            <tr>
                <td nowrap="nowrap">
                    <img height="16" width="16" class="button" src="/openerp/static/images/stock/gtk-go-back.png" 
                        onclick="getCalendar('${days[0].prev().isoformat()}', null)"/>
                </td>
                <td nowrap="nowrap">
                    <button type="button" title="${_('Today...')}" 
                        onclick="getCalendar('${days[0].today().isoformat()}', 'day')">${_("Today")}</button>
                </td>
                <td nowrap="nowrap">
                    <img height="16" width="16" class="button" src="/openerp/static/images/stock/gtk-go-forward.png" 
                        onclick="getCalendar('${days[-1].next().isoformat()}', null)"/>
                </td>
                <td nowrap="nowrap" width="100%"><strong>${title}</strong></td>
                <td nowrap="nowrap">
                    % if mode == 'day':
                    <img title="${_('Zoom In')}" height="16" width="16" src="/openerp/static/images/stock-disabled/gtk-zoom-in.png"/>
                    % endif
                    % if mode != 'day':
                    <img title="${_('Zoom In')}" height="16" width="16" class="button" src="/openerp/static/images/stock/gtk-zoom-in.png"
                        onclick="ganttZoomIn()"/>
                    % endif
                    
                    % if mode == '5years':
                    <img title="${_('Zoom Out')}" height="16" width="16" src="/openerp/static/images/stock-disabled/gtk-zoom-out.png"/>
                    % endif
                    % if mode != '5years':
                    <img title="${_('Zoom Out')}" height="16" width="16" class="button" src="/openerp/static/images/stock/gtk-zoom-out.png"
                        onclick="ganttZoomOut()"/>
                    % endif
                </td>
            </tr>
        </table>
        <input type="hidden" id="_terp_selected_day" name="_terp_selected_day" value="${selected_day.isoformat()}"/>
        <input type="hidden" id="_terp_selected_mode" name="_terp_selected_mode" value="${mode}"/>
        <input type="hidden" id="_terp_calendar_fields" name="_terp_calendar_fields" value="${calendar_fields}"/>
        <input type="hidden" id="_terp_gantt_level" name="_terp_gantt_level" value="${level}"/>
        % if concurrency_info:
            ${concurrency_info.display()}
        % endif
    </td>
</tr>
<tr>
    <td id="calMainArea" valign="top">

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
<tr>
    <td>        
        ${groupbox.display()}
        
        <div id="calSearchOptions">
            <table border="0">
                <tr>
                    <td>
                        <input type="checkbox" class="checkbox" 
                            id="_terp_use_search" name="_terp_use_search"
                            onclick="getCalendar()"
                            ${py.checker(use_search)}/>
                    </td>
                    <td><label for="_terp_use_search">${_("Apply search filter")}</label></td>
                </tr>
            </table>
        </div>

        <script type="text/javascript">
            CAL_INSTANCE = new GanttCalendar();
        </script>

    </td>
</tr>
</table>

