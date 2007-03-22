/**
 * Configuration settings for TinyAjax
 *
 */
var TinyAjaxConfig = {
	status: "Loading...",			// The message to display
	statusElem: "load_status",		// The element id in which message should be display
	target: null					// Target element id where result should go
}

/**
 * A wrapper arround MochiKit's doSimpleXMLHttpRequest method.
 * Provides a way to display Google style fancy "Loading..." message.
 *
 */
var TinyAjax = {

	/**
	 * A wrapper arround doSimpleXMLHttpRequest
	 *
	 * @param url the url
	 * @param params request paramas as map
	 * @param update the element id where result should go
	 * @param message the loading message
	 * @return differed object with wait(sec) function
	 *
	 */
	request: function(url, params, update, message) {

		$(TinyAjaxConfig.statusElem).innerHTML = message ? message : TinyAjaxConfig.status;
		$(TinyAjaxConfig.statusElem).style.display = "block";

		res = doSimpleXMLHttpRequest(url, params);

		res.addCallback(function(xmlHttp){
			target = update ? update : TinyAjaxConfig.target;
			if (target) {
				$(target).innerHTML = xmlHttp.responseText;
			}
		});

		res.addBoth(function(xmlHttp){
			$(TinyAjaxConfig.statusElem).style.display = "none";
		});

		res.wait = function(sec){
			return wait(sec, res);
		}

		return res;
	}
}

/**
 * A function to open centered popup window
 *
 */
function wopen(url, name, w, h) {
    var width = w ? w : 400;
    var height = h ? h : 300;
    var left = parseInt((screen.availWidth/2) - (width/2));
    var top = parseInt((screen.availHeight/2) - (height/2));
    var windowFeatures = "toolbar=0, statusbar=0, scrollbars=1" + ",width=" + width + ",height=" + height +
        ",status,resizable,left=" + left + ",top=" + top +
        "screenX=" + left + ",screenY=" + top;
    return window.open(url, name ? name : "popup", windowFeatures);
}

function URL(path, args) {
	return args ? path + "?" + queryString(args) : path;
}

