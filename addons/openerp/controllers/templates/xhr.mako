% for css in widget_css:
    ${css.display()}
% endfor
% for js in widget_javascript.get('head', []):
    ${js.display()}
% endfor
${next.header()}
% for js in widget_javascript.get('bodytop', []):
    ${js.display()}
% endfor
% for js in widget_javascript.get('bodybottom', []):
    ${js.display()}
% endfor
${self.content()}
