jQuery.noConflict();
jQuery(window).load(function(){
    var h = null, d = null;
    h = jQuery('#gs-group-messages-topic-add-privacy').html();
    d = {animation: true, html: true, placement: 'top', trigger: 'click', 
         content: h};
    jQuery('#gs-group-messages-topic-add-privacy-summary').popover(d);
});
