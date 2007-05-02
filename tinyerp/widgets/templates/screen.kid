<span xmlns:py="http://purl.org/kid/ns#">
    <input type="hidden" name="${name}_terp_model" value="${model}"/>
    <input type="hidden" name="${name}_terp_state" value="${state}"/>
    <input type="hidden" name="${name}_terp_id" value="${str(id)}"/>
    <input type="hidden" name="${name}_terp_ids" value="${str(ids)}"/>
    <input type="hidden" name="${name}_terp_view_ids" value="${str(view_ids)}"/>
    <input type="hidden" name="${name}_terp_view_mode" value="${str(view_mode)}"/>
    <input type="hidden" name="${name}_terp_view_mode2" value="${str(view_mode2)}"/>
    <input type="hidden" name="${name}_terp_domain" value="${str(domain)}"/>
    <input type="hidden" name="${name}_terp_context" value="${str(context)}"/>

    <span py:if="widget" py:replace="widget.display(value_for(widget), **params_for(widget))"/>
</span>