/**
 * Allowable width for the left-hand menu (for the current application)
 */
var MENU_WIDTH = 250;
/**
 * Tries to fit the size of the #appFrame frame to better fit its current
 * content.extend
 * Has to be called from the document outside of the frame itself.
 *
 * Probably won't get it exactly right, you might want to call it
 * several times
 */
function adjustAppFrame() {
    var frameHeight = jQuery("#appFrame").contents().find("body").height();
    var frameWidth = jQuery("#appFrame").contents().width();

    jQuery("#menubar").width(MENU_WIDTH);
    jQuery("#appFrame").height(Math.max(0, frameHeight));

    var menuWidth = jQuery("#menubar").height();
    var windowWidth = jQuery(window).width();
    var totalWidth = jQuery("#menubar").width() + frameWidth;
    var rw = windowWidth - jQuery("#menubar").width();

    var newWidth = totalWidth > windowWidth ? frameWidth : rw - 16;

    jQuery("#appFrame").width(Math.max(0, newWidth));
    jQuery("table#contents").height(Math.max(frameHeight, menuWidth));
}
