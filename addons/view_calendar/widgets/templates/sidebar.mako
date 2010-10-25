<div id="sidebar">
    <div class="sideheader-a">
        <h2>${_("Navigator")}</h2>
    </div>
    <div id="calMini">
        ${minical.display()}
    </div>
    <div id="calGroups">
        ${groupbox.display()}
    </div>
    <div class="sideheader-a">
        <h2>${_('Filter')}</h2>
    </div>
    <ul class="ul_calGroups">
        <li>
            <input type="checkbox" class="checkbox" id="_terp_use_search" 
                name="_terp_use_search" onclick="getCalendar()" ${py.checker(use_search)}/>
            <label for="_terp_use_search">${_("Apply search filter")}</label>
        </li>
    </ul>
</div>

