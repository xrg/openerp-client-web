<%
# put in try block to prevent improper redirection on connection refuse error
try:
    ROOT = cp.request.pool.get_controller("/openerp")
    SHORTCUTS = cp.request.pool.get_controller("/openerp/shortcuts")
    REQUESTS = cp.request.pool.get_controller("/openerp/requests")

    shortcuts = SHORTCUTS.my()
    requests, requests_message, total_mess = REQUESTS.my()
except:
    ROOT = None

    shortcuts = []
    requests = []
    requests_message = None
%>

<script type="text/javascript">
    function setRowWidth() {
        var top_divWidth = jQuery('div#top-menu').width();
        var logoWidth = jQuery('p#logo').outerWidth();

        var sc_rowWidth = top_divWidth - logoWidth - 10;
        jQuery('tr#sc_row').css('width', sc_rowWidth);
    }

    function showMore_sc(id, submenu) {
        var pos = jQuery('#'+id).position().left;

        jQuery('#'+submenu).css({
            'left': pos,
            'top': 25 + 'px'
        }).slideToggle('slow');
    }

    jQuery(document).ready(setRowWidth);
    jQuery(window).resize(setRowWidth);
</script>
<%
    if rpc.session.is_logged():
        header_class = "header_logged"
        logged = True
    else:
        header_class = "header_not_logged"
        logged = False
%>
<div id="top" class="${header_class}">
    <div id="top-menu">
        <p id="logo">
            <a href="http://www.openerp.com" target="_blank">
                <img alt="OpenERP" id="company_logo" src="/openerp/static/images/openerp_small.png"/>
            </a>
        </p>
        % if logged:
            <h1 id="title-menu">
               ${_("%(company_id)s", company_id=rpc.session.company_id or '')}
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
                    <li><a href="${py.url('/openerp/home')}" class="home">Home</a>
                        <ul>
                            <li class="first last"><a href="javascript: void(0);">Home</a></li>
                        </ul>
                    </li>

                    <li>
                        <a href="${py.url('/openerp/requests')}" class="messages">Messages<small>${total_mess}</small></a>
                        <ul>
                            <li class="first last"><a href="javascript: void(0);">Requests</a></li>
                        </ul>
                    </li>

                    <li><a href="${py.url('/openerp/pref/create')}" class="preferences">Preferences</a>
                        <ul>
                            <li class="first last"><a href="javascript: void(0);">Edit Preferences</a></li>
                        </ul>
                    </li>

                    <li><a href="javascript: void(0);" class="info">About</a>
                        <ul>
                            <li class="first last"><a href="javascript: void(0);">About</a></li>
                        </ul>
                    </li>

                    <li><a href="javascript: void(0);" class="help">Help</a>
                        <ul>
                            <li class="first last"><a href="javascript: void(0);">Help</a></li>
                        </ul>
                    </li>

                    % if cp.config('server.environment', 'openobject-web') == 'production':
                        <li id="clear_cache"><a href="${py.url('/openerp/pref/clear_cache')}" class="clear_cache">Clear Cache</a>
                            <ul>
                                <li class="first last"><a href="javascript: void(0);">Clear Cache</a></li>
                            </ul>
                        </li>
                    % endif
                </ul>
                <p class="logout"><a href="${py.url('/openerp/logout')}" target="_top">${_("Logout")}</a></p>
            </div>
        % endif
    </div>
    
    % if logged:
        <table id="shortcuts" class="menubar" cellpadding="0" cellspacing="0">
            <tr id="sc_row">
                % for i, sc in enumerate(shortcuts):
                    % if i < 7:
                        <td nowrap="nowrap">
                            <a href="${py.url('/openerp/tree/open', id=sc['res_id'], model='ir.ui.menu')}">${sc['name']}</a>
                        </td>
                    % endif
                % endfor
                % if len(shortcuts) >= 7:
                <td id="shortcuts_menu" nowrap="nowrap">
                    <a class="scMore_arrow" href="javascript: void(0)" 
                        onmouseover="showMore_sc('shortcuts_menu', 'shortcuts_submenu');">>></a>
                    <div class="submenu" id="shortcuts_submenu" onmouseover="showElement(this);" onmouseout="hideElement(this);">
                        % for sc in shortcuts[7:]:
                            <a href="${py.url('/openerp/tree/open', id=sc['res_id'], model='ir.ui.menu')}">${sc['name']}</a>
                        % endfor
                    </div>
                </td>
                % endif
            </tr>
        </table>
    % endif
</div>
