// GroupServer module for providing the Topics tab in a group.
jQuery.noConflict();
var GSStickyTopicToggle = function () {
    // Private variables
    var stickyToggle = null;
    var topicTitle = null;
    var loading = null;
    var done = null;
    // Constants
    var FADE_SPEED = 'slow';
    var FADE_METHOD = 'swing';
    var AJAX_PAGE = '../gs-group-messages-topic-sticky-setter';

    // Private methods
    var handle_change = function () {
        loading.fadeIn(FADE_SPEED, FADE_METHOD, do_toggle);
    };
    var do_toggle = function () {
        var data = null;
        var topicId = '';
        var sticky = null;
        
        topicId = topicTitle.attr('id');
        if (stickyToggle.val() == 'on') {
            sticky = '1';
        } else {
            sticky = '0';
        }
        
        data = {
            'topicId':    topicId,
            'sticky':     sticky,
        };
        jQuery.post(AJAX_PAGE, data, load_complete);
    };
    var load_complete = function (responseText, textStatus, request) {
        loading.fadeOut(FADE_SPEED, FADE_METHOD, show_done);
    };
    var show_done = function() {
        var m = null;
        if (stickyToggle.val() == 'on') {
            m = '<cite>'+topicTitle.text()+'</cite> is now sticky.';
        } else {
            m = '<cite>'+topicTitle.text()+'</cite> is now a normal topic.';
            
        }
        done.html(m)
            .fadeIn(FADE_SPEED, FADE_METHOD)
            .delay(1000)
            .fadeOut(FADE_SPEED, FADE_METHOD);
    };
    
    return {
        init: function () {
            stickyToggle = jQuery('#gs-group-messages-topic-admin-stickytoggle-widget-checkbox');
            stickyToggle.change(handle_change);
            loading = jQuery('#gs-group-messages-topic-admin-stickytoggle-loading');
            done = jQuery('#gs-group-messages-topic-admin-stickytoggle-done');
            topicTitle = jQuery('#gs-group-messages-topic-title cite');
        },
    };
}();
