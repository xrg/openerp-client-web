<span xmlns:py="http://purl.org/kid/ns#" py:strip="">
    <script py:if="editable" type="text/javascript">
        function ${name.replace('/', '_')}_clicked(sender){
            var getter = $('${name}');
            getter.value = sender.checked ? 1 : '';
			MochiKit.Signal.signal(getter, 'onchange');
        }
    </script>
    <input py:if="editable" type="hidden" kind="${kind}" name="${name}" id="${name}" value="${value}" py:attrs="attrs" callback="${callback}" onchange="${onchange}"/>
    <input py:if="editable" type="checkbox" class="checkbox" checked="${(value or None) and 1}" py:attrs="attrs" onclick="${name.replace('/', '_')}_clicked(this)"/>
    <span py:if="editable and error" class="fielderror" py:content="error"/>
    <input py:if="not editable" type="checkbox" class="checkbox" checked="${(value or None) and 1}" disabled="disabled"/>
</span>
