<div class="separator ${orientation}">${string}</div>
% if orientation == 'vertical':
    <script type="text/javascript">
        jQuery('.separator.vertical').parent().empty().addClass('separator vertical');
    </script>
%endif
