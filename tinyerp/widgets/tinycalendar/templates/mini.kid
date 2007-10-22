<div id="MiniCalendar" xmlns:py="http://purl.org/kid/ns#">
	<table class="calMini" width="100%" cellpadding="2" cellspacing="1" border="0">
		<tr class="calMiniHeader">
		    <td nowrap="nowrap"><img height="16" width="16" class="button" src="/static/images/stock/gtk-go-back.png" onclick="getMiniCalendar('${tg.url('/calendar/mini', year=month.prev().year, month=month.prev().month, forweek=forweek)}')"/></td>
		    <td nowrap="nowrap" width="100%" align="center" colspan="5">
		       <strong><a href="javascript: void(0)" onclick="getCalendar('/calendar/get/${month.year}/${month.month}'); return false;">${ustr(month)}</a></strong>
		    </td>
		    <td nowrap="nowrap"><img height="16" width="16" class="button" src="/static/images/stock/gtk-go-forward.png" onclick="getMiniCalendar('${tg.url('/calendar/mini', year=month.next().year, month=month.next().month, forweek=forweek)}')"/></td>    
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
		
		<tr py:for="week in month.weeks" class="calMiniDays ${(highlight and forweek and selected_day.week[0] == week[0] or None) and 'weekSelected'}">                   
		    <td class="${(day.month != month.month or None) and 'dayOff'} ${(day.today() == day or None) and 'dayThis'} ${(highlight and selected_day == day or None) and 'daySelected'}" py:for="day in week">                       
                <a href="javascript: void(0)" py:if="not forweek" onclick="getCalendar('/calendar/get/${day.isoformat()}'); return false;">${day.day}</a>
                <a href="javascript: void(0)" py:if="forweek" onclick="$('_terp_selected_day').value='${day.isoformat()}'; getCalendar('/calendar/get/${week[0].isoformat()}/${week[-1].isoformat()}'); return false;">${day.day}</a>
		    </td>
		</tr>
	</table>
</div>
