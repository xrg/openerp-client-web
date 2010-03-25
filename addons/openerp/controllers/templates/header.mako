<%
# put in try block to prevent improper redirection on connection refuse error
try:
    ROOT = cp.request.pool.get_controller("/")
    SHORTCUTS = cp.request.pool.get_controller("/shortcuts")
    REQUESTS = cp.request.pool.get_controller("/requests")
    
    shortcuts = SHORTCUTS.my()
    requests, requests_message, total_mess = REQUESTS.my()
except:

    ROOT = None
    
    shortcuts = []
    requests = []
    requests_message = None
%>
			
<div id="top">
	<p id="logo">
		<a href="javascript: void(0)" accesskey="h">
			<img src="/openerp/static/images/logo-a.gif" width="83px" height="26px"/>
		</a>
	</p>
	<h1 id="title">Tiny SPRL <small>Administration</small></h1>
		<ul id="skip-links">
		<li><a href="#nav" accesskey="n">Skip to navigation [n]</a></li>
		<li><a href="#content" accesskey="c">Skip to content [c]</a></li>
		<li><a href="#footer" accesskey="f">Skip to footer [f]</a></li>
	</ul>
	<div id="corner">
		<p class="name">${_("%(user)s", user=rpc.session.user_name or 'guest')}</p>
		<ul class="tools">
			<li>
				% if rpc.session.is_logged():
					<a target='appFrame' href="${py.url('/requests')}" class="messages">Messages<small>${total_mess}</small></a>
					<span class="inline"><strong>${total_mess} New Messages</strong></span>
				% endif
			</li>
			<li><a href="${py.url('/')}" class="home">Home</a></li>
			<li><a href="javascript: void(0)" class="shortcuts">Shortcuts</a>
				<ul>
					<li class="item">
						% for sc in shortcuts:
							<a target='appFrame' href="${py.url('/tree/open', id=sc['res_id'], model='ir.ui.menu')}">
							<small>${sc['name']}</small>
						% endfor
						</a>
					</li>
					<li class="last"><a target='appFrame' href="/shortcuts">Manage Shortcuts</a></li>
				</ul>
			</li>
			<li><a href="javascript: void(0)" class="preferences">Preferences</a>
				<ul>
					<li class="first last">
						<a target='appFrame' href="${py.url('/pref/create')}">Edit Preferences</a>
					</li>
				</ul>
			</li>
			<li><a href="javascript: void(0);" class="help">Help</a></li>
			<li><a href="javascript: void(0);" class="info">Info</a></li>
		</ul>
		<p class="logout"><a href="${py.url('/logout')}" target="_top">${_("Logout")}</a></p>
	</div>
</div>
