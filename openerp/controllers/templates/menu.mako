<%inherit file="base.mako"/>

<%def name="header()">
    <title>OpenERP</title>
    
    <link href="${py.url('/static/css/accordion.css')}" rel="stylesheet" type="text/css"/>
    <link href="${py.url('/static/css/treegrid.css')}" rel="stylesheet" type="text/css"/>
    
    <script type="text/javascript" src="${py.url('/static/javascript/menubar.js')}"></script>
    <script type="text/javascript" src="${py.url('/static/javascript/accordion.js')}"></script>
    <script type="text/javascript" src="${py.url('/static/javascript/treegrid.js')}"></script>
    
    <script type="text/javascript">

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
    </style>
    
</%def>

<%def name="content()">

    <%include file="header.mako"/>
    
    <table id="container">
        <tr>
            <td width="250">
                <div id="menubar_container">
                    <div id="menubar" class="accordion">
                    
                        % for tool in toolbar:
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
            <td>
                <div id="app_container">
                    <iframe width="100%" height="100%" border="0" frameborder="0" 
                        id="appFrame" name="appFrame" src="${py.url('/info')}"></iframe>
                </div>
            </td>
        </tr>
    </table>
    
</%def>

