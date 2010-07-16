<%
    if orientation:
        if position == 'vertical':
            css_class = "separator_vertical"
        else:
            css_class = "separator"    
    else:
        if position == 'vertical':
            css_class = "separator_vertical"
        else:
            css_class = "separator"
%>
<table class="${css_class}" height="100%">
   <tr>
        <td>${string}</td>
        <td></td>
    </tr>
</table>

% if position == 'vertical': 
<script type="text/javascript">
    jQuery('table.separator_vertical').parent().css('border-left','1px solid #666666');
</script>
% endif
