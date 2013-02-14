jQuery.noConflict();
function init_topic_share() {
    var buttons = null, i = 0, button = null, isPublic = false, 
        shareWidget = null;

    buttons = jQuery('.gs-content-js-share');
    for (i=0;i<buttons.length;i++) {
        button = buttons[i];
        // TODO: make isPublic not sux. This is the one topic-specific part.
        isPublic = Boolean(Number(jQuery(button).attr('public')));
        shareWidget = GSShareBox(button, isPublic);
        shareWidget.init();
    }
}

jQuery(window).load(function(){
    gsJsLoader.with_module('/++resource++gs-content-js-sharebox-min-20130114.js', 
                           init_topic_share);
});
