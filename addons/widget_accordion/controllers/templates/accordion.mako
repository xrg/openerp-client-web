<%inherit file="/openerp/controllers/templates/base.mako"/>

<%def name="header()">
    <title>${_("About the OpenERP Web")}</title>
    <title>Accordian</title>

    <script type="text/javascript" src="/widget_accordion/static/javascript/accordion.js"></script>    
    <link rel="stylesheet" href="/widget_accordion/static/css/accordion.css" type="text/css"/>
        

    <style>

    #container {
        border: 1px solid #6A4672;
        width: 250px;
        height: 400px;
        overflow: auto;
    }

    html, body, table {
        font-family: sans-serif;
        font-size: small;
    }

    </style>
        
</%def>

<%def name="content()">

<%include file="/openerp/controllers/templates/header.mako"/>        

    <div id="container">
    
    <div id="accordion">
    
        <div class="accordion-block">
            <h1 class="accordion-title">Strip One</h1>
            <div class="accordion-content">
                content would go here...
                <br>
                <br>
            </div>
        </div>
        
        <div class="accordion-block">
            <h1 class="accordion-title">Strip Two</h1>
            <div class="accordion-content">
                content would go here...
                <br>
                content would go here...
                <br>
                content would go here...
                <br>
                content would go here...
                <br>
                content would go here...
                <br>
                content would go here...
                <br>
                content would go here...
                <br>
                content would go here...
                <br>
            </div>
        </div>
        
        <div class="accordion-block">
            <h1 class="accordion-title">Strip Three</h1>
            <div class="accordion-content">
                content would go here...
                <br>
                content would go here...
                <br>
                content would go here...
                <br>
                content would go here...
                <br>
                content would go here...
                <br>
            </div>
        </div>
        
        <div class="accordion-block">
            <h1 class="accordion-title">Strip Four</h1>
            <div class="accordion-content">
                content would go here...
                <br>
                content would go here...
                <br>
                content would go here...
                <br>
                content would go here...
                <br>
                content would go here...
                <br>
                content would go here...
                <br>
                content would go here...
                <br>
            </div>
        </div>
        
        <div class="accordion-block">
            <h1 class="accordion-title">Strip Five</h1>
            <div class="accordion-content">
                content would go here...
                <br>
                content would go here...
                <br>
                content would go here...
                <br>
                content would go here...
                <br>
                content would go here...
                <br>
                content would go here...
                <br>
            </div>
        </div>
    
    </div>
    
    <script type="text/javascript">
    // <![CDATA[
        var ac = new Accordion('accordion', {
            duration: 0.3
        });
        
        MochiKit.Signal.connect(ac, "activate", function(accordion, title) {
            // `accordion` is the Accordion instance object
            // `title` is the activated title dom object
            
            /*
            
            so according to the current title, initialize Tree for the given
            accordion section.
            
            */
           
        });
    // ]]>
    </script>

    </div>
<%include file="/openerp/controllers/templates/footer.mako"/>       
</%def>

