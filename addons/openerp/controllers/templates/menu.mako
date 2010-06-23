<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>

<%def name="header()">
    <title>OpenERP</title>
    
    <link href="/openerp/static/css/treegrid.css" rel="stylesheet" type="text/css"/>
    <link href="/openerp/static/css/notebook.css" rel="stylesheet" type="text/css"/>

    <script type="text/javascript" src="/openerp/static/javascript/accordion.js"></script>
    <script type="text/javascript" src="/openerp/static/javascript/treegrid.js"></script>
    <script type="text/javascript" src="/openerp/static/javascript/notebook/notebook.js"></script>
    <script type="text/javascript" src="/openerp/static/javascript/scroll_scut.js"></script>

    <style type="text/css">
        .accordion-content {
        }

        .accordion {
            border: none;
        }

        .accordion-title {
            padding: 2px;
        }

        #menubar_container {
            overflow: auto;
            border: 1px solid black;
        }

        #content_iframe {
            overflow-x: auto;
            overflow-y: hidden;
        }

    </style>

    <script type="text/javascript">
        jQuery(document).ready(function() {
            var total_width = 0;
            jQuery('ul.sc_menu li').each(function() {
                total_width = parseFloat(total_width) + parseFloat(jQuery(this).css('width').split('px')[0]);
            });
            
            if(jQuery('div.sc_menu').width() > total_width) {
                jQuery('a.scroll_right').css('display', 'none');
            }
        });
        
        jQuery(document).ready(function() {
            resize_appContent()
        });
        
        function resize_appContent() {
            var window_width = jQuery(window).width();
            var secondary_width = jQuery('#secondary').width();
            var primary_width = window_width - secondary_width ;
            jQuery('#primary').width(primary_width - 50);
            
        }
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
							% if parent.get('action') and parent.get('active'):
							 <script type="text/javascript">
							     jQuery(document).ready(function() {
							     jQuery('#appContent').load(
							         openLink(openobject.http.getURL('/openerp/custom_action', {'action': "${parent['id']}"}))
							     )});
							 </script>
							% endif
						</li>
					% endfor
				</ul>
			</div>
		</div>
				
	    <div id="content" class="three-a">
		    <div id="secondary">
		    	<div class="wrap">
		    		<table class="sidenav-a">
				        <tr>
				            <td class="accordion-title-td">
				                <div id="menubar" class="accordion">
				                    % for tool in tools:
				                    <div class="accordion-block" id="block_${tool['id']}">
				                        <table class="accordion-title" id="title_${tool['id']}">
				                            <tr>
				                                <td id="${tool['id']}" class="accordion-title-td" >
                                                % if tool.get('action_id'):
                                                  <a href="${py.url('/openerp/custom_action', action=tool['action_id'])}">
                                                    ${tool['name']}</a>
                                                % else:
                                                  <span>${tool['name']}</span>
                                                % endif
                                              </td>
				                            </tr>
				                        </table>
				                        <div class="accordion-content" id="content_${tool['id']}">
				                            ${tool['tree'].display()}
				                        </div>
				                    </div>
				                    % endfor
				                </div>
				                <script type="text/javascript">
				                    new Accordion("menubar");
				                </script>
				            </td>
		           		</tr>
		        	</table>
		    	</div>
			</div>
			<div class="hide_tools" style="display: none;">
                 <script type="text/javascript">
                    jQuery('div.hide_tools').click(function() {
                        jQuery(this).toggleClass('show_tools hide_tools')
                        if(jQuery(this).attr('class') == 'show_tools') {
                            jQuery('#secondary').width(0);
                            jQuery('#secondary').hide()
                        }
                        else {
                            jQuery('#secondary').width(180);
                            jQuery('#secondary').show()
                        }
                        
			            resize_appContent()
                    });
                 </script>
             </div>
			<div id="primary">
			    
				<div class="wrap">
					<div id="appContent"></div>
					% if setup:
					   <script type="text/javascript">
					   openLink(openobject.http.getURL('/openerp/home'));
					   </script>
					% endif
				</div>
			</div>
		</div>
	</div>
</%def>

