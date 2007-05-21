<span xmlns:py="http://purl.org/kid/ns#" py:strip="">
    <script type="text/javascript">
        function ${name.replace('/', '_')}_clicked(sender){
            var getter = $('${name}');

            getter.value = sender.checked ? 1 : '';
            
            if (typeof getter.onchange != 'undefined'){
                getter.onchange();
            }
        }
    </script>
    <input type="hidden" kind="${kind}" name="${name}" id="${name}" value="${value}" callback="${callback}" onchange="${onchange}"/>
    <input type="checkbox" class="checkbox" checked="${(value or None) and 1}" onclick="${name.replace('/', '_')}_clicked(this)"/>
    <span class="fielderror" py:if="error" py:content="error"/>
</span>
