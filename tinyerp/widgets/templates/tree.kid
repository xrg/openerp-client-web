<div xmlns:py="http://purl.org/kid/ns#" id="${id}">
	<script language="javascript">
		//XXX: xTree cookies conficts with eTiny cookies and session
		webFXTreeConfig.usePersistence = false;	 // disable cookie support

		var ${id}_tree = new WebFXLoadTree('${title}', '${url}/${model}/-1?action=${action}&amp;target=${target}');
		document.write(${id}_tree);
	</script>
</div>
