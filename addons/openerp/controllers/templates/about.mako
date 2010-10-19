<%inherit file="/openerp/controllers/templates/base_dispatch.mako"/>

<%def name="header()">
    <title>${_("About the OpenERP Web")}</title>
</%def>

<%def name="content()">

<table class="view" width="100%">
    <tr>
        <td>

<table width="100%">
        <tr>
            <td class="titlebar"><h1>${_("OpenERP Web")}</h1></td>
        </tr>
        <tr>
            <td>
            <b>${version}</b>
<p>
${_("Copyright &copy; 2006-TODAY Tiny ERP Pvt. Ltd. All Rights Reserved.")|n}<br/>
${_("OpenERP is a trademark of the Tiny Company.")}

${_("%(ooweb)s is jointly developed by %(tiny)s and %(axelor)s.",
    ooweb="""<i>OpenERP Web</i>""",
    tiny="""<a target="_blank" href="http://tiny.be">Tiny</a>""",
    axelor="""<a target="_blank" href="http://www.axelor.com/">Axelor</a>""")|n}
</p>

<p>
${_("Licenced under the terms of %(license)s", license="""<a href="/LICENSE.txt">OpenERP Public License (OEPL) v1.1</a>""")|n}
</p>

            </td>
        </tr>
        <tr>
            <td width="100%" class="titlebar"><h1>${_("About OpenERP")}</h1></td>
        </tr>
        <tr>
            <td>
<p>
${_("""%(openobject)s is a free enterprise-scale software system that is designed to boost
productivity and profit through data integration. It connects, improves and
manages business processes in areas such as sales, finance, supply chain,
project management, production, services, CRM, etc..
""", openobject="""<a target="_blank" href="http://openerp.com/">OpenERP</a>""")|n}
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
        <tr>
            <td width="100%" class="titlebar"><h1>${_("Links")}</h1></td>
        </tr>
        <tr>
            <td>
<ul>
    <li><a target="_blank" href="http://www.openerp.com/">OpenERP</a></li>
    <li><a target="_blank" href="http://www.axelor.com/">${_("The Axelor Company")}</a></li>
    <li><a target="_blank" href="http://tiny.be/">${_("The Tiny Company")}</a></li>
</ul>
            </td>
        </tr>
   </table>

        </td>
        <td width="170" valign="top" id="sidebar">
            <table cellpadding="0" cellspacing="0" border="0" class="sidebox" width="100%">
                <tr>
                    <td class="sidebox-title">
                        <table border="0" cellpadding="0" cellspacing="0" width="100%">
                            <tr>
                                <td width="8"  class="sidebox-title-l"/>
                                <td class="sidebox-title-m">${_("RESOURCES")}</td>
                                <td width="35" class="sidebox-title-r"/>
                            </tr>
                        </table>
                    </td>
                </tr>
                <tr>
                    <td>
                        <a target="_blank" href="http://www.openerp.com/">${_("Homepage")}</a>
                    </td>
                </tr><tr>
                    <td>
                        <a target="_blank" href="http://www.openerp.com/downloads">${_("Download")}</a>
                    </td>
                </tr><tr>
                    <td>
                        <a target="_blank" href="http://doc.openerp.com/">${_("Documentation")}</a>
                    </td>
                </tr><tr>
                    <td>
                        <a target="_blank" href="http://doc.openerp.com/py-modindex.html">${_("Modules")}</a>
                    </td>
                </tr><tr>
                    <td>
                        <a target="_blank" href="http://www.openerp.tv/">${_("Screencasts")}</a>
                    </td>
                </tr><tr>
                    <td>
                        <a target="_blank" href="http://www.openerp.com/community">${_("Community")}</a>
                    </td>
                </tr><tr>
                    <td>
                        <a target="_blank" href="http://www.openerp.com/online">${_("SaaS Offers")}</a>
                    </td>
                </tr><tr>
                    <td>
                        <a target="_blank" href="http://www.openerp.com/services/trainings">${_("Trainings")}</a>
                    </td>
                </tr><tr>
                    <td>
                        <a target="_blank" href="http://www.openerp.com/services">${_("Services")}</a>
                    </td>
                </tr>
            </table>
        </td>
    </tr>
</table>

</%def>
