<div id="footer">
${_("Copyright &copy; 2007-TODAY Tiny ERP Pvt. Ltd. All Rights Reserved.")|n}
${_("More Information on %s") % ("""<a target="_blank" href="http://openerp.com">http://openerp.com</a>.""")|n}
<br/>
${_("The web client is developed by %(axelor)s and %(tiny)s.", 
    tiny="""Tiny (<a target="_blank" href="http://tiny.be">http://tiny.be</a>)""",
    axelor="""Axelor (<a target="_blank" href="http://axelor.com">http://axelor.com</a>)""")|n}
<br/>
${_("Running Server:")} <span>${rpc.session.protocol}://${rpc.session.host}:${rpc.session.port} - database: ${rpc.session.db or 'N/A'}</span><br/>
</div>
