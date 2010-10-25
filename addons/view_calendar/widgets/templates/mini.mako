<%
def css_class(i, off=False):
    res = []
    if i == 0: res.append('first')
    if i == 6: res.append('last')
    if off: res.append('off')
    return ' '.join(res)
%>

<div class="minical-a">
    <h3>
        <a class="prev" href="javascript: void(0)"
            onclick="getMiniCalendar('${py.url('/view_calendar/calendar/mini', 
                year=month.prev().year, month=month.prev().month, forweek=forweek)}')">Previous</a>
        ${month}
        <a class="next" href="javascript: void(0)"
            onclick="getMiniCalendar('${py.url('/view_calendar/calendar/mini',
                year=month.next().year, month=month.next().month, forweek=forweek)}')">Next</a>
    </h3>    
    <table summery="Calendar">
        % for week in month.weeks:
        <tr>
            % for i, day in enumerate(week):
            <td class="${css_class(i, day.month != month.month)}">
                % if not forweek:
                <a href="javascript: void(0)" 
                    onclick="getCalendar('${day.isoformat()}', 'day'); return false;">${day.day}</a>
                % endif
                % if forweek:
                <a href="javascript: void(0)" 
                    onclick="openobject.dom.get('_terp_selected_day').value='${day.isoformat()}';
                        getCalendar('${day.isoformat()}', 'week'); return false;">${day.day}</a>
                % endif
            </td>
            % endfor
        </tr>
        % endfor
    </table>
</div>

