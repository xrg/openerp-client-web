<%inherit file="/openerp/controllers/templates/base.mako"/>

<%def name="header()">
    <title>OpenERP</title>

    <link href="/openerp/static/css/accordion.css" rel="stylesheet" type="text/css"/>
    <link href="/openerp/static/css/treegrid.css" rel="stylesheet" type="text/css"/>
    <link href="/openerp/static/css/notebook.css" rel="stylesheet" type="text/css"/>

    <script type="text/javascript" src="/openerp/static/javascript/accordion.js"></script>
    <script type="text/javascript" src="/openerp/static/javascript/treegrid.js"></script>
    <script type="text/javascript" src="/openerp/static/javascript/notebook/notebook.js"></script>

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

    <%include file="header.mako"/>

    <div id="menutabs" class="notebook menu-tabs">
        %for parent in parents:
        <div id="${parent['id']}" title="${parent['name']}"></div>
        %endfor
    </div>

    <script type="text/javascript">

        var nb = new Notebook('menutabs', {
            'closable': false,
            'scrollable': true
        });

        MochiKit.Signal.connect(nb, 'click', function(nb, tab) {
            window.location.href = openobject.http.getURL("/menu", {active: tab.id});
        });

    </script>

    <table id="contents" width="100%">
        <tr>
            <td width="250" valign="top">
                <div id="menubar" class="accordion">
                    % for tool in tools:
                        <div class="accordion-block">
                            <table class="accordion-title">
                                <tr>
                                    <td><img alt="" src="${tool['icon']}" width="16" height="16" align="left"/></td>
                                    <td id="${tool['id']}">${tool['name']}</td>
                                    % if tool.get('action_id'):
                                    	<script type="text/javascript">
                                    	jQuery("#${tool['id']}").click(function() {
                                    		jQuery('#appFrame').attr("src", openobject.http.getURL('/tree/open', {'model': "ir.ui.menu", 'id': "${tool['action_id']}"}))
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
            <td valign="top">
                <div id="appContent"></div>
            </td>
        </tr>
    </table>
    
    <%include file="footer.mako"/>
</%def>

