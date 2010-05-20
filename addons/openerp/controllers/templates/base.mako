<%inherit file="/openobject/controllers/templates/base.mako"/>

<%def name="header()">
    <script type="text/javascript" src="/openerp/static/javascript/openerp/openerp.ui.js"></script>
    <script type="text/javascript" src="/openerp/static/javascript/openerp/openerp.ui.tips.js"></script>
    <script type="text/javascript" src="/openerp/static/javascript/ajax_stat.js"></script>
    <script type="text/javascript" src="/openerp/static/javascript/scripts.js"></script>
    
    <link type="image/x-icon" href="favicon.ico" rel="Shortcut Icon"/>
    
    <link rel="stylesheet" type="text/css" href="/openerp/static/css/style.css"/>
    <link rel="stylesheet" type="text/css" href="/openerp/static/css/menu.css"/>
    <link rel="stylesheet" type="text/css" href="/openerp/static/css/tips.css"/>
    <link rel="stylesheet" type="text/css" href="/openerp/static/css/screen.css"/>
    
    <!--[if IE]>
    <link rel="stylesheet" type="text/css" href="/openerp/static/css/style-ie.css"/>
    <![endif]-->
    
    <script type="text/javascript">
    
        var frame = window.frameElement ? window.frameElement.name : null;
        
        if (frame == "appFrame") {
            with (parent) {
                jQuery("#appFrame").width(0).height(0);
            }
        }
        
    </script>
    
    ${self.header()}
</%def>

