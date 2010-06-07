<table border="0" style="border: none;" id="Calendar">
	<tr>
		<td><div id="calLoading">${_("Loading...")}</div></td>
	</tr>
	<tr>
		<td width="100%" style="width: 100%; padding: 0;">
			<div class="box-a calendar-a">
			<p class="side">
				<a class="button-b" href="javascript:void(0)" title="${_('Today...')}" onclick="getCalendar('${selected_day.today().isoformat()}', 'day')">${_("Today")}</a>
			</p>
			<ul class="head">
				<li>
					<a href="javascript: void(0)" title="${_('Month Calendar...')}" onclick="getCalendar(null, 'month')">${_("Month")}</a>
				</li>
				<li>
					<a class="active" href="javascript: void(0)" title="${_('Week Calendar...')}">${_("Week")}</a>
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
						<a class="prev" href="javascript: void(0)" onclick="getCalendar('${week.prev()[0].isoformat()}')"></a>
					</span>
					<small>|</small>
					<span class="two">
						<a class="next" href="javascript: void(0)" onclick="getCalendar('${week.next()[0].isoformat()}')"></a>
						<small>|</small>
						<a class="last" href="javascript: void(0)"></a>
					</span>
				</p>
				<h4>
					<span>
						<small>${week}</small>
					</span>
				</h4>
			</div>
			<table border="0" id="calContainer" width="100%">
				<tr>
					<td id="calMainArea" valign="top">
						<input type="hidden" id="_terp_selected_day" name="_terp_selected_day" value="${selected_day.isoformat()}"/>
        <input type="hidden" id="_terp_selected_mode" name="_terp_selected_mode" value="week"/>
        <input type="hidden" id="_terp_calendar_fields" name="_terp_calendar_fields" value="${calendar_fields}"/>
        % if concurrency_info:
            ${concurrency_info.display()}
        % endif
				        <div id="calWeek" class="calWeek" dtFormat="${date_format}"><span></span>

            <div id="calHeaderSect">
                % for day in week:
                <div dtDay="${day.isoformat()}">${day.name} ${day.day}</div>
                % endfor
            </div>

            <div id="calAllDaySect">
                % for evt in events:
                    % if evt.dayspan > 0:
                <div nRecordID="${evt.record_id}" nDaySpan="${evt.dayspan}" dtStart="${str(evt.starts)}" dtEnd="${str(evt.ends)}" title="${evt.description}" style="background-color: ${evt.color}; -moz-border-radius: 5px;" class="calEvent allDay">${evt.title}</div>
                    % endif
                % endfor
            </div>

            <div id="calBodySect">
                % for evt in events:
                    % if evt.dayspan == 0:
                <div nRecordID="${evt.record_id}" dtStart="${str(evt.starts)}" dtEnd="${str(evt.ends)}" style="background-color: ${evt.color}; -moz-border-radius: 5px;" class="calEvent noAllDay">
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
	<div id="tertiary">
                <div id="tertiary_wrap">
                    <table id="sidebar_pane" cellspacing="0" cellpadding="0" border="0">
                        <tr>
                            <td id="sidebar_calendar" style="display: none;">
                                <table id="calSidebar-sidebar">
                                    <tr>
                                        <td class="sideheader-a">
                                            <h2>Navigator</h2>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 0;">
                                            <div id="mini_calendar">
                                                ${minical.display()}
                                            </div>
                                            <div id="group_box">
                                                ${groupbox.display()}
                                            </div>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td id="calendar_search_filter">
                                            <div id="calSearchOptions">
                                                <dl>
                                                    <dt>${_("Filter")}</dt>
                                                    <dd>
                                                        <ul class="ul_calGroups">
                                                            <li>
                                                                <input type="checkbox" class="checkbox" id="_terp_use_search" name="_terp_use_search" onclick="getCalendar()" ${py.checker(use_search)}/>
                                                                <label>${_("Apply search filter")}</label>
                                                            </li>
                                                        </ul>
                                                    </dd>
                                                </dl>
                                            </div>
                                        </td>
                                    </tr>
                                </table>
                          </td>
                          <td id="sidebar_calendar_hide" valign="top" style="padding: 0;">
                              <p class="toggle-a">
                                  <a id="toggle-click" class="on" href="javascript: void(0)">
                                      Toggle
                                  </a>
                                  <script type="text/javascript">
                                    jQuery('#toggle-click').click(function() {
                                        jQuery('#toggle-click').toggleClass('off');
                                        jQuery('#sidebar_calendar').toggle();
                                        CAL_INSTANCE.onResize();
                                    });
                                  </script>
                              </p>
                          </td>
                      </tr>
                  </table>
              </div>
          </div>
</td>
	</tr>
</table>