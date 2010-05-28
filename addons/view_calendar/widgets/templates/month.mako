<table border="0" style="border: none;" id="Calendar">
<tr>
		<td><div id="calLoading">${_("Loading...")}</div></td>
	</tr>
<tr>
	<td>
	
<div class="box-a calendar-a">
	<p class="side">
		<a class="button-b" href="javascript:void(0)" title="${_('Today...')}" onclick="getCalendar('${selected_day.today().isoformat()}', 'day')">${_("Today")}</a>
	</p>
	<ul class="head">
		<li>
			<a class="active" href="javascript: void(0)" title="${_('Month Calendar...')}">${_("Month")}</a>
		</li>
		<li>
			<a href="javascript: void(0)" title="${_('Week Calendar...')}" onclick="getCalendar(null, 'week')">${_("Week")}</a>
		</li>
		<li>
			<a href="javascript: void(0)" title="${_('Day Calendar...')}" onclick="getCalendar(null, 'day')">${_("Day")}</a>
		</li>
	</ul>
	<div class="inner">
		<p class="paging-a">
			<span class="one">
				<a class="first" href="javascript: void(0)"></a>
				<small>|</small>
				<a class="prev" href="javascript: void(0)" onclick="getCalendar('${month.prev().year}-${month.prev().month}-01')"></a>
			</span>
			<small>|</small>
			<span class="two">
				<a class="next" href="javascript: void(0)" onclick="getCalendar('${month.next().year}-${month.next().month}-01')"></a>
				<small>|</small>
				<a class="last" href="javascript: void(0)"></a>
			</span>
		</p>
		<h4>
			<span>
				<small>${month}</small>
			</span>
		</h4>
	</div>
	<table border="0" id="calContainer" width="100%">
		<tr>
				<td id="calMainArea" valign="top">
				<input type="hidden" id="_terp_selected_day" name="_terp_selected_day" value="${selected_day.isoformat()}"/>
	<input type="hidden" id="_terp_selected_mode" name="_terp_selected_mode" value="month"/>
	<input type="hidden" id="_terp_calendar_fields" name="_terp_calendar_fields" value="${calendar_fields}"/>
	% if concurrency_info:
		${concurrency_info.display()}
	% endif
        <div id="calMonth" class="calMonth" dtFormat="${date_format}" dtStart="${month[0].isoformat()}" dtFirst="${month.year}-${month.month}-01"><span></span>

            <div id="calHeaderSect">
                % for day in month.weeks[0]:
                    <div class="calDayName">${day.name}</div>
                % endfor
            </div>

            <div id="calBodySect">
                % for evt in events:
                    % if evt.dayspan > 0:
                    <div class="calEvent"
                         nRecordID="${evt.record_id}"
                         nDaySpan="${evt.dayspan}"
                         dtStart="${str(evt.starts)}"
                         dtEnd="${str(evt.ends)}"
                         title="${evt.description}"
                         style="background-color: ${evt.color}">${evt.title}</div>
                    % endif
                    % if evt.dayspan == 0:
                    <div class="calEvent calEventInfo"
                         nRecordID="${evt.record_id}"
                         nDaySpan="${evt.dayspan}"
                         dtStart="${str(evt.starts)}"
                         dtEnd="${str(evt.ends)}"
                         title="${evt.description}"
                         style="color: ${evt.color}">${evt.starts.strftime('%H:%M')} - ${evt.title}</div>
                    % endif
                % endfor
            </div>
        </div>

        <script type="text/javascript">
            CAL_INSTANCE = new MonthCalendar();
        </script>

    </td>
		</tr>
	</table>
</div>
</td>
<td id="calSidebar"valign="top">
	<table>
		<tr>
			<td class="toggle-a" align="right">
				<a  id="toggle-navigator" class="on" href="javascript: void(0)" style="float: right;">Toggle</a>
				
				<script type="text/javascript">
					jQuery('#toggle-navigator').click(function() {
						jQuery('#toggle-navigator').toggleClass('off');
						jQuery('#calSidebar-sidebar').toggle();
					});
				</script>
			</td>
		</tr>
	</table>
	<table id="calSidebar-sidebar">
		<tr>
			<td class="sideheader-a">
				<h2>Navigator</h2>
			</td>
		</tr>
		<tr>
			<td>
				${minical.display()}
			</td>
		</tr>
		<tr>
			<td>
				${groupbox.display()}
			</td>
		</tr>
		<tr>
			<td>
				<div id="calSearchOptions">
            <table border="0">
                <tr>
                    <td><input type="checkbox" class="checkbox" id="_terp_use_search" name="_terp_use_search" onclick="getCalendar()" ${py.checker(use_search)}/></td>
                    <td>${_("Apply search filter")}</td>
                </tr>
		</table>
        </div>
			</td>
		</tr>
	</table>
</td>
</tr>
</table>
