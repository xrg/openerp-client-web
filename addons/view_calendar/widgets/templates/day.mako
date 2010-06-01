<table border="0" style="border: none;" id="Calendar">
	<tr>
		<td><div id="calLoading">${_("Loading...")}</div></td>
	</tr>
	<tr>
		<td>
			<div class="box-a calendar-a">
				<p class="side">
					% if day == day.today():
                		<a class="button-a" href="javascript: void(0)">${_("Today")}</a>
               		% else:
               			<a class="button-b" href="javascript: void(0)" onclick="getCalendar('${day.today().isoformat()}', 'day')">${_("Today")}</a>
					% endif
				</p>
				<ul class="head">
					<li>
						<a href="javascript: void(0)" title="${_('Month Calendar...')}" onclick="getCalendar(null, 'month')">${_("Month")}</a>
					</li>
					<li>
						<a href="javascript: void(0)" title="${_('Week Calendar...')}" onclick="getCalendar(null, 'week')">${_("Week")}</a>
					</li>
					<li>
						<a class="active" href="javascript: void(0)" title="${_('Day Calendar...')}">${_("Day")}</a>
					</li>
				</ul>
				<div class="inner">
					<p class="paging-a">
						<span class="one">
							<a class="first" href="javascript: void(0)"></a>
							<small>|</small>
							<a class="prev" href="javascript: void(0)" onclick="getCalendar('${day.prev().isoformat()}')"></a>
						</span>
						<small>|</small>
						<span class="two">
							<a class="next" href="javascript: void(0)" onclick="getCalendar('${day.next().isoformat()}')"></a>
							<small>|</small>
							<a class="last" href="javascript: void(0)"></a>
						</span>
					</p>
					<h4>
						<span>
							<small>${day}</small>
						</span>
					</h4>
				</div>
				<table border="0" id="calContainer" width="100%">
					<tr>
						<td id="calMainArea" valign="top">
							<input type="hidden" id="_terp_selected_day" name="_terp_selected_day" value="${day.isoformat()}"/>
					        <input type="hidden" id="_terp_selected_mode" name="_terp_selected_mode" value="day"/>
					        <input type="hidden" id="_terp_calendar_fields" name="_terp_calendar_fields" value="${calendar_fields}"/>
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
                <div nRecordID="${evt.record_id}" nDaySpan="${evt.dayspan}" dtStart="${str(evt.starts)}" dtEnd="${str(evt.ends)}" title="${evt.description}" style="background-color: ${evt.color}" class="calEvent allDay">${evt.title}</div>
                    % endif
                % endfor
            </div>

            <div id="calBodySect">
                % for evt in events:
                    % if evt.dayspan == 0:
                <div nRecordID="${evt.record_id}" dtStart="${str(evt.starts)}" dtEnd="${str(evt.ends)}" style="background-color: ${evt.color}" class="calEvent noAllDay">
                   <div style="height: 10px;" class="calEventTitle">${evt.starts.strftime('%I:%M %P')} - ${evt.title}</div>
                   <div class="calEventDesc">${evt.description}</div>
                   <div class="calEventGrip"></div>
                </div>
                    % endif
                % endfor
            </div>
					        </div>
					        <script type="text/javascript">
            CAL_INSTANCE = new WeekCalendar();
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