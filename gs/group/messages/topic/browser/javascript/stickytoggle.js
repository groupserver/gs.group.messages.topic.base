// GroupServer module for providing the Topics tab in a group.
jQuery.noConflict();
var GSStickyTopicToggle = function () {
    // Private variables
    var stickyToggle = null;
    var loading = null;
    var done = null;
    // Constants
    var FADE_SPEED = 'slow';
    var FADE_METHOD = 'swing';

    // Private methods
    var handle_change = function () {
        loading.fadeIn(FADE_SPEED, FADE_METHOD, do_toggle);
    };
    var do_toggle = function () {
        //jQuery.post(ajaxPage, data, load_complete);
        load_complete('foo', 'bar', 'wibble');
    };
    var load_complete = function (responseText, textStatus, request) {
        loading.fadeOut(FADE_SPEED, FADE_METHOD, show_done);
    };
    var show_done = function() {
        done.fadeIn(FADE_SPEED, FADE_METHOD)
            .delay(1000).fadeOut(FADE_SPEED, FADE_METHOD);
    };
    
    return {
        init: function () {
            stickyToggle = jQuery('#gs-group-messages-topic-admin-stickytoggle-widget-checkbox');
            stickyToggle.change(handle_change);
            loading = jQuery('#gs-group-messages-topic-admin-stickytoggle-loading');
            done = jQuery('#gs-group-messages-topic-admin-stickytoggle-done');
        },
    };
}();
