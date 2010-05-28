<%inherit file="/openerp/controllers/templates/base.mako"/>

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

</%def>

<%def name="content()">

	<div id="root">
	    <%include file="header.mako"/>
	    
	    <div id="main_nav">
		    <a id="scroll_left" class="scroll_right" style="text-align: center; width: 2%; float: left; padding-top: 12px;" href="javascript: void(0);">
		    	<img src="/openerp/static/images/scroll_left.png"></img>
		    </a>
		    <a id="scroll_right" class="scroll_right" style="text-align: center; width: 2%; float: right; margin-right: 0; padding: 12px 5px 0 0;" href="javascript: void(0);">
		    	<img src="/openerp/static/images/scroll_right.png"></img>
		    </a>
		    <div id="nav" class="sc_menu">
				<ul class="sc_menu">
					%for parent in parents:
						<li id="${parent['id']}" class="menu_tabs"">
							<a href="javascript: void(0)" accesskey="1" class="${parent['active']}">
								<span>${parent['name']}</span>
							</a>
							<em>[1]</em>
						</li>
					% endfor
				</ul>
			</div>
		</div>
				
	    <script type="text/javascript">
	    
	    	var tabs = MochiKit.DOM.getElementsByTagAndClassName('li', "menu_tabs");
	        
	        MochiKit.Iter.forEach(tabs, function(tab) {
	        	MochiKit.Signal.connect(tab, 'onclick', function(){
		            window.location.href = openobject.http.getURL("/openerp/menu", {active: tab.id});
		        });
	        });
	        
	    </script>
	    
	    <div id="content" class="three-a">
		    <div id="secondary">
		    	<div class="wrap">
		    		<table class="sidenav-a">
				        <tr>
				            <td class="accordion-title-td">
				                <div id="menubar" class="accordion">
				                    % for tool in tools:
				                    <div class="accordion-block">
				                        <table class="accordion-title">
				                            <tr>
				                                <td class="accordion-title-td" id="${tool['id']}"><a href="javascript: void(0);">${tool['name']}</a></td>
                                                % if tool.get('action_id'):
                                                    <script type="text/javascript">
                                                        jQuery("#${tool['id']}").click(function() {
                                                            jQuery('#appFrame').attr("src", openobject.http.getURL('/openerp/tree/open', {'model': "ir.ui.menu", 'id': "${tool['id']}"}))
                                                        });
                                                    </script>
                                                % endif
				                            </tr>
				                        </table>
				                        <div class="accordion-content">
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
			
			<div id="primary">
				<div class="wrap">
					% if setup:
	                    <iframe id="appFrame" width="100%"
	                        scrolling="no"
	                        frameborder="0"
	                        name="appFrame" src="${py.url('/openerp/home')}"></iframe>
	                % else:
	                    <iframe id="appFrame" width="100%"
	                        scrolling="no"
	                        frameborder="0"
	                        name="appFrame"></iframe>
	                % endif
				</div>
			</div>
		</div>
	</div>
</%def>

