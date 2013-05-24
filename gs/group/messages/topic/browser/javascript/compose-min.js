jQuery.noConflict();function GSFileUpload(e,d,b){var a='<abbr class="muted" title="Remove this file from the list of files">(remove)</abbr>';
function c(j){var k=jQuery(".MultiFile-applied"),l="",g="",h=null,f=null;for(h=0;
h<k.length;h++){f=jQuery(k[h]);l=f.attr("id");g=l+"."+h;f.attr("id",g).attr("name",g)
}return true}return{init:function(){var f={list:b,STRING:{remove:a}};jQuery(d).MultiFile(f);
jQuery(e).submit(c)}}}function gs_group_messages_topic_multifile_init(){var a=null;
a=GSFileUpload(".gs-group-messages-topic-add","#form\\.uploadedFile",".gs-group-messages-topic-add-file-files-list");
a.init()}jQuery(window).load(function(){var a=null,b=null;if(jQuery(".gs-group-messages-topic-add").length!=0){a=jQuery("#gs-group-messages-topic-add-privacy").html();
b={animation:true,html:true,placement:"top",trigger:"click",content:a};jQuery("#gs-group-messages-topic-add-privacy-summary").popover(b);
gsJsLoader.with_module("/++resource++multiple_file_upload-1.48/jquery.MultiFile.js",gs_group_messages_topic_multifile_init)
}});