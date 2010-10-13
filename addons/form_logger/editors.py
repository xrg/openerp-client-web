# -*- coding: utf-8 -*-


import openobject.templating

class FormEditor(openobject.templating.TemplateEditor):
    templates = ['/openerp/widgets/templates/sidebar.mako']
    SIDEBAR_START = u'<div id="sidebar">'

    def edit(self, template, template_text):
        output = super(FormEditor, self).edit(template, template_text)

        insertion_point = output.index(self.SIDEBAR_START) + len(self.SIDEBAR_START)
        return output[:insertion_point] + '''
            % if view_type == 'form':
                <div class="sideheader-a">
                    <h2>Piratepad</h2></div>
                <ul class="clean-a">
                    % if piratepad:
                        <li><a href="http://piratepad.net/${piratepad['pad']}" target="_blank">${piratepad['name']}</a></li>
                    % else:
                        <li><a href="#" id="add-piratepad" class="button-a">${_("Add")}</a></li>
                    % endif
                </ul>
            % endif
        ''' + output[insertion_point:]
