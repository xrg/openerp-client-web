<%
# put in try block to prevent improper redirection on connection refuse error
try:
    ROOT = cp.request.pool.get_controller("/openerp")
    SHORTCUTS = cp.request.pool.get_controller("/openerp/shortcuts")
    REQUESTS = cp.request.pool.get_controller("/openerp/requests")

    shortcuts = SHORTCUTS.my()
    requests, total_request = REQUESTS.my()
except:
    ROOT = None

    shortcuts = []
    requests = []
    requests_message = None

if rpc.session.is_logged():
    logged = True
else:
    logged = False
%>
<td id="top" colspan="3">
    <p id="cmp_logo">
        <a href="http://www.openerp.com" target="_blank">
            <img alt="OpenERP" id="company_logo" src="/openerp/static/images/openerp_small.png"/>
        </a>
    </p>
    % if logged:
        <h1 id="title-menu">
           ${_("%(company_id)s", company_id=rpc.session.company_id or '')} (${rpc.session.db})
           <small>${_("%(user)s", user=rpc.session.user_name)}</small>
        </h1>
    % endif
    <ul id="skip-links">
        <li><a href="#nav" accesskey="n">Skip to navigation [n]</a></li>
        <li><a href="#content" accesskey="c">Skip to content [c]</a></li>
        <li><a href="#footer" accesskey="f">Skip to footer [f]</a></li>
    </ul>
    % if logged:
	    <div id="corner">
	        <ul class="tools">
	            <li><a href="javascript: void(0)" onclick="header_actions('/openerp/home')" class="home">${_("Home")}</a>
	                <ul>
	                    <li class="first last"><a href="javascript: void(0)" onclick="header_actions('/openerp/home')">${_("Home")}</a></li>
	                </ul>
	            </li>
	            <li>
	                <a href="javascript: void(0)" onclick="header_actions('/openerp/requests')" class="req_messages"><small>${total_request}</small></a>
	                <ul>
	                    <li class="first last"><a href="javascript: void(0)" onclick="header_actions('/openerp/requests')">${_("Requests")}</a></li>
	                </ul>
	            </li>

	            <li><a href="javascript: void(0)" onclick="header_actions('/openerp/pref/create')" class="preferences">${_("Preferences")}</a>
	                <ul>
	                    <li class="first last"><a href="javascript: void(0)" onclick="header_actions('/openerp/pref/create')">${_("Edit Preferences")}</a></li>
	                </ul>
	            </li>
	            <li><a href="javascript: void(0)" onclick="header_actions('/openerp/about')" class="info">${_("About")}</a>
	                <ul>
	                    <li class="first last"><a href="javascript: void(0)" onclick="header_actions('/openerp/about')">${_("About")}</a></li>
	                </ul>
	            </li>

	            <li><a target="_blank" href="http://doc.openerp.com/" class="help">${_("Help")}</a>
	                <ul>
	                    <li class="first last"><a target="_blank" href="http://doc.openerp.com/">${_("Help")}</a></li>
	                </ul>
	            </li>

	            % if cp.config('server.environment') == 'production':
	                <li id="clear_cache"><a href="javascript: void(0)" onclick="header_actions('/openerp/pref/clear_cache')" class="clear_cache">${_("Clear Cache")}</a>
	                    <ul>
	                        <li class="first last"><a href="javascript: void(0);">${_("Clear Cache")}</a></li>
	                    </ul>
	                </li>
	            % endif
	        </ul>
	        <p class="logout"><a href="${py.url('/openerp/logout')}" target="_top">${_("Logout")}</a></p>
	    </div>
	% endif
	
    <div id="shortcuts" class="menubar">
    % if logged:
        <ul>
	        % for i, sc in enumerate(shortcuts):
	            <li class="${i == 0 and 'first' or ''}">
	                <a id="shortcut_${sc['res_id']}"
	                   href="javascript: void(0)"
                       onclick='header_actions("/openerp/tree/open","${sc['res_id']}", "ir.ui.menu")'>
	                   <span>${sc['name']}</span>
	                </a>
	            </li>
	        % endfor
        </ul>
    % endif
    </div>
</td>
