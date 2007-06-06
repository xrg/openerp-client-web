<div class="pager" xmlns:py="http://purl.org/kid/ns#">    
    <button py:attrs="buttons['first']" type="button" onclick="submit_search_form('first')">First</button>
    <button py:attrs="buttons['prev']" type="button" onclick="submit_search_form('previous')">Preious</button>
    <button class="button" type="button" py:strip=""><b>(${offset} to ${offset + total})</b></button>
    <button py:attrs="buttons['next']" type="button" onclick="submit_search_form('next')">Next</button>
    <button py:attrs="buttons['last']" type="button" onclick="submit_search_form('last')">Last</button>
</div>
