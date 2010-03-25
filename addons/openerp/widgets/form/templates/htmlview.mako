
% if tag_name and tag_name != "html":
	<${tag_name} ${py.attrs(args)}>
		% for child in children:
	    	${display_member(child)}
	    % endfor
	    % if value:
	    	${value | n}
	    % endif
	</${tag_name}>
% elif tag_name == "html":
	% for child in children:
    	${display_member(child)}
    % endfor
% else:
	${value | n}
% endif
