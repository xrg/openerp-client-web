<div id="MiniCalendar">
    <table class="calMini" width="100%" cellpadding="2" cellspacing="1" border="0">
        <tr class="calMiniHeader">
            <td nowrap="nowrap"><img height="16" width="16" class="button" src="/openerp/static/images/stock/gtk-go-back.png" onclick="getMiniCalendar('${py.url('/view_calendar/calendar/mini', year=month.prev().year, month=month.prev().month, forweek=forweek)}')"/></td>
            <td nowrap="nowrap" width="100%" align="center" colspan="5">
               <strong><a href="javascript: void(0)" onclick="getCalendar('${month.year}-${month.month}-01', 'month'); return false;">${month}</a></strong>
            </td>
            <td nowrap="nowrap"><img height="16" width="16" class="button" src="/openerp/static/images/stock/gtk-go-forward.png" onclick="getMiniCalendar('${py.url('/view_calendar/calendar/mini', year=month.next().year, month=month.next().month, forweek=forweek)}')"/></td>
        </tr>
        <tr class="calMiniTitles">
           <td>M</td>
           <td>T</td>
           <td>W</td>
           <td>T</td>
           <td>F</td>
           <td>S</td>
           <td>S</td>
        </tr>

        % for week in month.weeks:
        <tr class="calMiniDays ${(highlight and forweek and selected_day.week[0] == week[0] or None) and 'weekSelected'}">
            % for day in week:
            <td class="${(day.month != month.month or None) and 'dayOff'} ${(day.today() == day or None) and 'dayThis'} ${(highlight and selected_day == day or None) and 'daySelected'}">
                % if not forweek:
                <a href="javascript: void(0)" onclick="getCalendar('${day.isoformat()}', 'day'); return false;">${day.day}</a>
                % endif
                % if forweek:
                <a href="javascript: void(0)" onclick="openobject.dom.get('_terp_selected_day').value='${day.isoformat()}'; getCalendar('${day.isoformat()}', 'week'); return false;">${day.day}</a>
                % endif
            </td>
            % endfor
        </tr>
        % endfor
    </table>
</div>

