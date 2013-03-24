jQuery.noConflict();function GSFileUpload(e,d,b){var a='<abbr class="muted" title="Remove this file from the list of files">(remove)</abbr>';
function c(j){var k=jQuery(".MultiFile-applied"),l="",g="",h=null,f=null;for(h=0;
h<k.length;h++){f=jQuery(k[h]);l=f.attr("id");g=l+"."+h;f.attr("id",g).attr("name",g)
}return true}return{init:function(){var f={list:b,STRING:{remove:a}};jQuery(d).MultiFile(f);
jQuery(e).submit(c)}}}function init_multifile(){var a=null;a=GSFileUpload(".gs-group-messages-topic-add","#form\\.uploadedFile",".gs-group-messages-topic-add-file-files-list");
a.init()}jQuery(window).load(function(){var a="/++resource++multiple_file_upload-1.48/jquery.MultiFile.js";
if(jQuery(".gs-group-messages-topic-add").length!=0){gsJsLoader.with_module(a,init_multifile)
}});