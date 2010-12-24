<%inherit file="/openerp/controllers/templates/openm2.mako"/>
<%def name="relation()">m2m</%def>
<%def name="default_load_counter()">0</%def>
<%def name="token_to_close(token)">${token} && [${token}]</%def>
