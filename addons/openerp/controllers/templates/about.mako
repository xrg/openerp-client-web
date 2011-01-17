<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>

<%def name="header()">
    <title>${_("About the OpenERP Web")}</title>
    <style type="text/css">
        #body_form a {
            color: blue;
        }
        #body_form p {
            font-size: 120%;
            padding:0 5px 5px;
        }
        
        ul {
            list-style: none;
        }
        
        ul a.cta-a{
            color: #8C8C8C !important;
        }
    </style>
</%def>
<%def name="content()">
    <table class="view" width="100%" cellspacing="0" cellpadding="0" border="0">
        <tr>
            <td id="body_form" colspan="2">
                <h1>${_("OpenERP Web")}</h1>
                <h3 style="padding:0 5px 5px">${version}</h3>
                <p>
                    ${_("Copyright &copy; 2006-TODAY OpenERP SA. All Rights Reserved.")|n}<br/>
                    ${_("OpenERP is a trademark of the OpenERP SA Company.")}
                    
                    ${_("%(ooweb)s is jointly developed by %(tiny)s and %(axelor)s.",
                        ooweb="""<i>OpenERP Web</i>""",
                        tiny="""<a target="_blank" href="http://www.openerp.com" style="text-decoration: underline;">OpenERP</a>""",
                        axelor="""<a target="_blank" href="http://www.axelor.com/" style="text-decoration: underline;">Axelor</a>""")|n}
                </p>
                <p>
                    ${_("Licenced under the terms of %(license)s", license="""<a target="_blank" href="/LICENSE.txt" style="text-decoration: underline;">OpenERP Public License (OEPL) v1.1</a>""")|n}
                </p>
                <br>
                <h1>${_("About OpenERP")}</h1>
                <p>
                    ${_("""%(openobject)s is a free enterprise-scale software system that is designed to boost
                    productivity and profit through data integration. It connects, improves and
                    manages business processes in areas such as sales, finance, supply chain,
                    project management, production, services, CRM, etc..
                    """, openobject="""<a target="_blank" href="http://openerp.com/" style="text-decoration: underline;">OpenERP</a>""")|n}
                </p>
                <p>
                    ${_("""The system is platform-independent, and can be installed on Windows, Mac OS X,
                    and various Linux and other Unix-based distributions. Its architecture enables
                    new functionality to be rapidly created, modifications to be made to a
                    production system and migration to a new version to be straightforward.""")}
                </p>
                <p>
                    ${_("""Depending on your needs, OpenERP is available through a web or application client.""")}
                </p>
            </td>
        </tr>
    </table>
</%def>
