<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>

<%def name="header()">
    <title>OpenERP</title>
    
    <link href="/openerp/static/css/treegrid.css" rel="stylesheet" type="text/css"/>
    <link href="/openerp/static/css/notebook.css" rel="stylesheet" type="text/css"/>

    <script type="text/javascript" src="/openerp/static/javascript/accordion.js"></script>
    <script type="text/javascript" src="/openerp/static/javascript/treegrid.js"></script>
    <script type="text/javascript" src="/openerp/static/javascript/notebook/notebook.js"></script>
    <script type="text/javascript" src="/openerp/static/javascript/scroll_scut.js"></script>

    <script type="text/javascript">
        var DOCUMENT_TO_LOAD = "${load_content}";
        var CAL_INSTANCE = null;
        
        jQuery(document).ready(function() {
            var total_width = 0;
            jQuery('ul.sc_menu li').each(function() {
                total_width = parseFloat(total_width) + parseFloat(jQuery(this).css('width').split('px')[0]);
            });
            
            if(jQuery('div.sc_menu').width() > total_width) {
                jQuery('a.scroll_right').css('display', 'none');
            }
        });

        jQuery(document).ready(function () {
            // Don't load doc if there is a hash-url, it takes precedence
            if(DOCUMENT_TO_LOAD && !hashUrl()) {
                openLink(DOCUMENT_TO_LOAD);
            }

            jQuery('.open-close-menu').click(function() {
                jQuery('#content').toggleClass('hide-menu');
                jQuery(window).trigger('on-appcontent-resize');
            });
        });
        
    </script>
</%def>

<%def name="content()">

    <div id="root">
        <%include file="header.mako"/>
        
        <div id="main_nav">
            <a id="scroll_left" class="scroll_right" style="float: left; padding-top: 12px;" href="javascript: void(0);">
                <img src="/openerp/static/images/scroll_left.png" alt="">
            </a>
            <a id="scroll_right" class="scroll_right" style="float: right; margin-right: 0; padding: 12px 5px 0 0;" href="javascript: void(0);">
                <img src="/openerp/static/images/scroll_right.png" alt="">
            </a>
            <div id="nav" class="sc_menu">
                <ul class="sc_menu">
                    %for parent in parents:
                        <li id="${parent['id']}" class="menu_tabs">
                            <a href="${py.url('/openerp/menu', active=parent['id'])}" target="_top" class="${parent.get('active', '')}">
                                <span>${parent['name']}</span>
                            </a>
                            <em>[1]</em>
                        </li>
                    % endfor
                </ul>
            </div>
        </div>
                
        <div id="content" class="three-a">
            <div id="secondary" class="sidenav-open">
                <div class="wrap">
                    <ul id="sidenav-a" class="accordion">
                        % for tool in tools:
                            % if tool.get('action'):
                              <li class="accordion-title" id="${tool['id']}">
                            % else:
                              <li class="accordion-title">
                            % endif
                                <span>${tool['name']}</span>
                            </li>
                            <li class="accordion-content" id="content_${tool['id']}">
                               ${tool['tree'].display()}
                            </li>
                        % endfor
                    </ul>
                    <script type="text/javascript">
                        new Accordion("sidenav-a");
                    </script>
                </div>
            </div>
            <div class="open-close-menu hide_tools"></div>
            <div id="primary">
                <div class="wrap">
                    <div id="appContent"></div>
                </div>
            </div>
        </div>
    </div>
</%def>

