% for w in hiddens:
<div style="display: none;">${display_member(w)}</div>
% endfor

<table border="0" class='fields' width="100%">
    % for row in table:
    <tr>
        % for attrs, widget  in row:
        <td ${py.attrs(attrs)}>
            % if isinstance(widget, basestring):
                % if attrs.get('label_position'):
                <table id="search_table">
                    <tr>
                        <td ${py.attrs(attrs.get('widget_item')[0])} width="${attrs.get('width')}">
                            <label for="${attrs.get('for')}">
                                ${(widget or '') and widget}
                            </label>
                            % if attrs.get('title'):
                                <sup style="color: darkgreen; vertical-align: middle;">?</sup>
                            % endif
                            :
                        </td>
                    </tr>
                    <tr>
                         <td ${py.attrs(attrs.get('widget_item')[0])} width="${attrs.get('width')}">
                                % if attrs.get('widget_item')[1].kind in ('char', 'selection', 'one2many', 'many2many'):
                                    <table>
                                        <tr>
                                            <td class="filter_item">
                                                ${display_member(attrs.get('widget_item')[1])}
                                            </td>
                                        </tr>
                                    </table>
                                % else:
                                    ${display_member(attrs.get('widget_item')[1])}
                                % endif
                         </td>
                    </tr>
                </table>
                % else:
                    ${(widget or '') and widget}
                    % if attrs.get('title'):
                        <sup style="color: darkgreen;">?</sup>
                    % endif
                    :
                % endif
            % endif
            % if not isinstance(widget, basestring) and widget.visible:
            ${display_member(widget)}
            % endif
        </td>
        % endfor
    </tr>
    % endfor
</table>

