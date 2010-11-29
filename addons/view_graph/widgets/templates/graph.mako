<input type="hidden" id="_terp_search_callback" value="reload_graph">
<div class="graph-block" style="text-align: center; padding: 5px; min-width: ${width}px;">
    <div id="${name}_" class="flash-chart"></div>
    
    <script type="text/javascript">
        charts['${name}'] = ${data|n};
        // Client side hack. Should find a better way to do this.
        if (jQuery('#name').eq(0).val().toLowerCase() != 'dashboard') {
            charts['${name}']['bg_colour'] = '#F0EEEE';
        }
    </script>
</div>

