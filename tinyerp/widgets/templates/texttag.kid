<span xmlns:py="http://purl.org/kid/ns#">
	<textarea
    	name="${name}"
        class="${field_class}"
        id="${field_id}"
        rows="700"
        cols="40"
        style="width:100%; display: none"
        py:attrs="attrs"
        py:content="value"
	/>
	<span class="fielderror" py:if="error" py:content="error"/>
	<script language="javascript">
	 tinyMCE.init({
        mode: "exact",
        theme: "advanced",
        elements: "${name}",
        plugins : "fullscreen,print",
		fullscreen_new_window : false,
		fullscreen_settings : {theme_advanced_path_location : "top"},
        theme_advanced_disable : "styleselect",
        theme_advanced_toolbar_location : "top",
        theme_advanced_toolbar_align : "left",
        extended_valid_elements : "a[href|target|name]",
        theme_advanced_resizing : false,
        height : "400",
        paste_use_dialog : false,
        paste_auto_cleanup_on_paste : true,
        paste_convert_headers_to_strong : false,
        paste_strip_class_attributes : "all",
    });

	</script>
</span>