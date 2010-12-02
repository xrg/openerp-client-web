<input type="hidden" id="${name}_terp_string" name="${name}_terp_string" value="${string}"/>
<input type="hidden" id="${name}_terp_model" name="${name}_terp_model" value="${model}"/>
<input type="hidden" id="${name}_terp_state" name="${name}_terp_state" value="${state}"/>
<input type="hidden" id="${name}_terp_id" name="${name}_terp_id" value="${id}"/>
<input type="hidden" id="${name}_terp_ids" name="${name}_terp_ids" value="${ids}"/>

<input type="hidden" id="${name}_terp_view_ids" name="${name}_terp_view_ids" value="${view_ids}"/>
<input type="hidden" id="${name}_terp_view_mode" name="${name}_terp_view_mode" value="${view_mode}"/>
<input type="hidden" id="${name}_terp_view_type" name="${name}_terp_view_type" value="${view_type}"/>
<input type="hidden" id="${name}_terp_view_id" name="${name}_terp_view_id" value="${view_id}"/>
<input type="hidden" id="${name}_terp_domain" name="${name}_terp_domain" value="${domain}"/>
<input type="hidden" id="${name}_terp_context" name="${name}_terp_context" value="${ctx}"/>
<input type="hidden" id="${name}_terp_editable" name="${name}_terp_editable" value="${editable}"/>

<input type="hidden" id="${name}_terp_limit" name="${name}_terp_limit" value="${limit}"/>
<input type="hidden" id="${name}_terp_offset" name="${name}_terp_offset" value="${offset}"/>
<input type="hidden" id="${name}_terp_count" name="${name}_terp_count" value="${count}"/>
<input type="hidden" id="${name}_terp_group_by_ctx" name="${name}_terp_group_by_ctx" value="${group_by_ctx}"/>
<input type="hidden" id="${name}_terp_filters_context" name="${name}_terp_filters_context" value=""/>

% if widget:
    ${display_member(widget)}
% endif
