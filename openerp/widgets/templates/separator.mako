%if orientation:
	<table class="separator_vertical" height="100%">
	   <tr>
	        <td>${string}</td>
	        <td></td>
	    </tr>
	</table>
%else:
	<table class="separator" width="100%">
	    <tr>
	        <td>${string}</td>
	        <td></td>
	    </tr>
	</table>
%endif