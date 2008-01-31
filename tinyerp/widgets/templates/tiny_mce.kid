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
            
            theme: "advanced",
            plugins: "fullscreen,print",
            
            content_css: "/static/css/texttag.css",
            apply_source_formatting : true,
            
            extended_valid_elements : "a[href|target|name]",
            theme_advanced_disable : "styleselect",
            
            ${buttons},
                                                
            //theme_advanced_statusbar_location : "bottom",
            //theme_advanced_resizing : true,
            //theme_advanced_resize_horizontal : false,
            
            height: 350,
            debug: false
        });    
    </script>
    
</span>
