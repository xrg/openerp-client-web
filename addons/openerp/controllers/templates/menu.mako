<%inherit file="/openerp/controllers/templates/base.mako"/>

<%def name="header()">
    <title>OpenERP</title>
    
    <link href="/openerp/static/css/accordion.css" rel="stylesheet" type="text/css"/>
    <link href="/openerp/static/css/treegrid.css" rel="stylesheet" type="text/css"/>
    <link href="/openerp/static/css/notebook.css" rel="stylesheet" type="text/css"/>
    
    <script type="text/javascript" src="/openerp/static/javascript/menubar.js"></script>
    <script type="text/javascript" src="/openerp/static/javascript/accordion.js"></script>
    <script type="text/javascript" src="/openerp/static/javascript/treegrid.js"></script>
    <script type="text/javascript" src="/openerp/static/javascript/notebook/notebook.js"></script>
    
    <script type="text/javascript">
       
        function load_menu(id) {
    		window.location.href = openobject.http.getURL("/menu2", {p_id: id});
    	}
    	
    	MochiKit.DOM.addLoadEvent(function(evt){
            window.MAIN_WINDOW = true;
        });
    	
    	function onload_frame() {
    		ifrm = getElement('content_iframe');
	        if (ifrm) {
	        	if (window.frames['appFrame'].document.getElementById('main_form_body')) {
	        		getElement('content_iframe').style.height = elementDimensions(window.frames['appFrame'].document.getElementById('main_form_body')).h + 'px';
	        		//getElement('content_iframe').style.width = elementDimensions(window.frames['appFrame'].document.getElementById('main_form_body')).w + 'px';
	        	}
	       	}
    	}
    	
</script>
    
    <style>
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

    <%include file="header2.mako"/>
	    <div for="static_menu_tabs" style="display: block; border-top: 1px solid gray;" align="center" valign="top">
	    	<div id="static_menu_tabs" class="notebook">
	    		% for tool in toolbar:
	    			<div id="${tool['id']}" title="${tool['name']}"></div>
	    		% endfor
	    	</div>
	    	<script type="text/javascript">
	    		
	    		var tabClick = function(nb, tab){
	    			load_menu(tab.id);
	    		}
	    		
                var nb = new Notebook('static_menu_tabs', {
                	'closable': false,
                	'scrollable': true
                });
                
                MochiKit.Signal.connect(nb, 'click', tabClick);
	    		
               </script>
		</div>
    
    % if show_formview:
    <table id="container" cellspacing="0" cellpadding="2" border="0" width="100%">
        <tr>
            <td width="250">
                <div id="menubar_container">
                    <div id="menubar" class="accordion">
                        % for tool in new_toolbar:
                        <div class="accordion-block">
                            <table class="accordion-title">
                                <tr>
                                    % if tool['icon']:
                                    <td><img src="${tool['icon']}" width="16" height="16" align="left"/></td>
                                    % endif
                                    <td>${tool['name']}</td>
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
                </div>
            </td>
            <td style="height: 100%">
                <div id="app_container" height="100%">
                    <iframe id="content_iframe" width="100%" height="100%" border="0" frameborder="0" 
                        name="appFrame" src="${py.url('/info')}"></iframe>
                </div>
            </td>
        </tr>
    </table>
    % endif
</%def>

