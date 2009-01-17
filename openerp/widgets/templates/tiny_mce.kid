<span xmlns:py="http://purl.org/kid/ns#" py:strip="">
    <textarea
        id="${field_id}" name="${name}" kind="${kind}"
        class="${field_class}" style="width: 100%;"
        py:attrs="attrs" py:content="value"></textarea>
    <span class="fielderror" py:if="editable and error" py:content="error"/>
    
    <script type="text/javascript">
        tinyMCE.init({
            mode: "exact",
            elements: "${name}",
            editor_selector: "tinymce",
            readonly: ${(not editable or 0) and 1},
            
            theme: "advanced",

            plugins: "fullscreen,print,safari",
            
            content_css: "${tg.url('/static/css/tiny_mce.css')}",
            apply_source_formatting : true,
            
            extended_valid_elements : "a[href|target|name]",

            theme_advanced_disable : "styleselect",
            theme_advanced_toolbar_location : "top",
            theme_advanced_buttons3_add : "|,print,fullscreen",
            theme_advanced_statusbar_location : "bottom",
            theme_advanced_resizing : true,
            theme_advanced_resize_horizontal : false,

            tab_focus : ':prev,:next',
            height: 350,
            debug: false
        });
    </script>
    
</span>
