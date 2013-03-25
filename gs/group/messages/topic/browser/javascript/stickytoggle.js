// GroupServer module for providing the Topics tab in a group.
jQuery.noConflict();
var GSStickyTopicToggle = function (getBase, topicId, stickyToggle) {
    // Constants
    var AJAX_PAGE = getBase + 'gs-group-messages-topic-sticky-setter', 
        GET_PAGE = getBase + 'gs-group-messages-topic-sticky-getter';

    // Private methods
    function do_toggle() {
        var data = null, sticky = null;

        stickyToggle.button('loading');
        if (stickyToggle.hasClass('active')) {
            sticky = '0';
        } else {
            sticky = '1';
        }
        
        data = {
            'topicId':    topicId,
            'sticky':     sticky
        };
        jQuery.post(AJAX_PAGE, data, show_done);
    };

    function show_done(responseText, textStatus, request) {
        if (stickyToggle.hasClass('active')) {
            stickyToggle.button('sticky');
        } else {
            stickyToggle.button('normal');
        }
        window.setTimeout(set_normal, 5000);
    }

    function set_normal() {
        stickyToggle.button('reset');
    }

    function set_checkbox(responseText, textStatus, request) {
        if (responseText == '1') {
            stickyToggle.button('toggle');
        }
        stickyToggle.removeAttr('disabled');
    }
    
    return {
        init: function () {
            stickyToggle.click(do_toggle);
            jQuery.post(GET_PAGE, {'topicId': topicId}, set_checkbox);
        }//init
    };
};

jQuery(window).load(function (event) {
    var toggle = null, baseUrl = null, getBase = null, stickyToggle = null, 
        topicId = null;

    baseUrl = jQuery('base').attr('href');
    getBase = baseUrl.slice(0, baseUrl.indexOf('topic'));
    stickyToggle = jQuery('#gs-group-messages-topic-admin-stickytoggle button');
    topicId = jQuery('#gs-group-messages-topic-title cite').attr('id');
    toggle = GSStickyTopicToggle(getBase, topicId, stickyToggle);
    toggle.init();
});
