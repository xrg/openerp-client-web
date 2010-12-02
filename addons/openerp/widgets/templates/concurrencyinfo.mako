% if ids and model in info:
    % for id in ids:
        % if id in info[model]:
            <input type="hidden" name="_terp_concurrency_info"
                   id="${model.replace('.', '-')}-${id}"
                   value="('${model},${id}', '${info[model][id]}')"/>
        % endif
    % endfor
% endif
