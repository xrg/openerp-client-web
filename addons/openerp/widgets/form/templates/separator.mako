<%
    if orientation == 'vertical':
        css_class = "separator_vertical"
    else:
        css_class = "separator"
%>
<table class="${css_class}" height="100%">
   <tr>
        <td style="padding: 2px 0px;">${string}</td>
        <td></td>
    </tr>
</table>

% if orientation == 'vertical':
<script type="text/javascript">
    jQuery('table.separator_vertical').parent().empty().css('border-left','1px solid #666666');
</script>
%endif
