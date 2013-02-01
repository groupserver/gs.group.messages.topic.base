jQuery.noConflict();
jQuery(document).ready(function(){
    var buttons = null;
    var i = 0;
    var button = null;
    var public = false;
    var shareWidget = null;

    buttons = jQuery('.gs-content-js-share');
    for (i=0;i<buttons.length;i++) {
        button = buttons[i];
        // TODO: make public not sux. This is the one topic-specific part.
        public = Boolean(Number(jQuery(button).attr('public')));
        shareWidget = GSShareBox(button, public);
        shareWidget.init();
    }
});
