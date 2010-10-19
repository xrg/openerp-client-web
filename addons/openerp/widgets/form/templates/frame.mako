% for w in hiddens:
<div style="display: none;">${display_member(w)}</div>
% endfor

<table border="0" class='fields' width="100%">
    % for row in table:
    <tr>
        % for attrs, widget  in row:
        <td ${py.attrs(attrs)}>
            % if isinstance(widget, basestring):
                <% widget_item = attrs['widget_item'][1] %>
                % if attrs.get('is_search'):
                    <table class="search_table">
                        <tr>
                            <td ${py.attrs(attrs.get('widget_item')[0])} width="${attrs.get('width')}">
                                ${widget_item.label.display()}
                            </td>
                        </tr>
                        <tr>
                             <td ${py.attrs(attrs.get('widget_item')[0])} width="${attrs.get('width')}">
                                % if widget_item.kind in ('char', 'selection', 'one2many', 'many2many'):
                                    <span class="filter_item">
                                        ${display_member(widget_item)}
                                    </span>
                                % else:
                                    ${display_member(widget_item)}
                                % endif
                                % for filter_widget in attrs.get('widget_item')[1].filters:
                                    ${display_member(filter_widget)}
                                % endfor
                             </td>
                        </tr>
                    </table>
                % else:
                    ${widget_item.label.display()}
                % endif
            % elif widget.visible:
                ${display_member(widget)}
            % endif
        </td>
        % endfor
    </tr>
    % endfor
</table>

