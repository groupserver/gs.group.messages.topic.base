jQuery.noConflict();

var GSTopicButtons = function () {
    // Private variables
    var NAVLINKS = '.gs-group-messages-topic-navlinks';
    var prev = {icons: { primary: "ui-icon-carat-1-w" }, text: true};
    var up = {icons: { primary: "ui-icon-arrowthick-1-n" }, text: false};
    var next = {icons: { secondary: "ui-icon-carat-1-e" }, text: true};

    return {
        init: function() {
            jQuery(NAVLINKS + ' .prev').button(prev);
            jQuery(NAVLINKS + ' span.prev').button("disable");
            jQuery(NAVLINKS + ' .up').button(up);
            jQuery(NAVLINKS + ' .next').button(next);
            jQuery(NAVLINKS + ' span.next').button("disable");
            
            jQuery('#form\\.actions\\.post').button();
        }//init
    };
}();
