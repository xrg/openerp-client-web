<div class="pager" xmlns:py="http://purl.org/kid/ns#">    
    <button py:attrs="buttons['first']" type="button" onclick="submit_search_form('first')">&lt;&lt; First</button>
    <button py:attrs="buttons['prev']" type="button" onclick="submit_search_form('previous')">&lt; Preious</button>
    <button class="button" type="button">(${offset} to ${offset + total})</button>
    <button py:attrs="buttons['next']" type="button" onclick="submit_search_form('next')">Next &gt;</button>
    <button py:attrs="buttons['last']" type="button" onclick="submit_search_form('last')">Last &gt;&gt;</button>
</div>
