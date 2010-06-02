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
		    	<img src="/openerp/static/images/scroll_left.png" alt="">
		    </a>
		    <a id="scroll_right" class="scroll_right" style="text-align: center; width: 2%; float: right; margin-right: 0; padding: 12px 5px 0 0;" href="javascript: void(0);">
		    	<img src="/openerp/static/images/scroll_right.png" alt="">
		    </a>
		    <div id="nav" class="sc_menu">
				<ul class="sc_menu">
					%for parent in parents:
						<li id="${parent['id']}" class="menu_tabs">
							<a href="${py.url('/openerp/menu', active=parent['id'])}" target="_top" class="${parent.get('active')}">
								<span>${parent['name']}</span>
							</a>
							<em>[1]</em>
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
				                    <div class="accordion-block">
				                        <table class="accordion-title">
				                            <tr>
				                                <td id="${tool['id']}" class="accordion-title-td" >
                                                % if tool.get('action_id'):
                                                  <a href="${py.url('/tree/open', model='ir.ui.model', id=tool['action_id'])}">
                                                    ${tool['name']}</a>
                                                % else:
                                                  <span>${tool['name']}</span>
                                                % endif
                                              </td>
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
					<div id="appContent"></div>
				</div>
			</div>
		</div>
	</div>
</%def>

