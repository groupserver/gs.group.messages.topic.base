jQuery.noConflict();
jQuery(document).ready(function(){
    var h = null;
    var d = null;
    h = jQuery('#gs-group-messages-topic-add-privacy').html();
    d = {animation: true, html: true, placement: 'top', trigger: 'click', 
         content: h};
    jQuery('#gs-group-messages-topic-add-privacy-summary').popover(d);
});
