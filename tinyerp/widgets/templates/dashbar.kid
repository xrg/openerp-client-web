<div class="dashbar" xmlns:py="http://purl.org/kid/ns#">
	<div class="dashlet" py:for="child in children" 
	py:content="child.display(value_for(child), **params_for(child))"/>
</div>