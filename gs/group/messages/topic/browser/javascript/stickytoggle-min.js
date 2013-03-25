jQuery.noConflict();var GSStickyTopicToggle=function(b,g,f){var e=b+"gs-group-messages-topic-sticky-setter",i=b+"gs-group-messages-topic-sticky-getter";
function d(){var j=null,k=null;f.button("loading");if(f.hasClass("active")){k="0"
}else{k="1"}j={topicId:g,sticky:k};jQuery.post(e,j,a)}function a(k,l,j){if(f.hasClass("active")){f.button("sticky")
}else{f.button("normal")}window.setTimeout(c,5000)}function c(){f.button("reset")
}function h(k,l,j){if(k=="1"){f.button("toggle")}f.removeAttr("disabled")}return{init:function(){f.click(d);
jQuery.post(i,{topicId:g},h)}}};jQuery(window).load(function(f){var c=null,e=null,b=null,a=null,d=null;
e=jQuery("base").attr("href");b=e.slice(0,e.indexOf("topic"));a=jQuery("#gs-group-messages-topic-admin-stickytoggle button");
d=jQuery("#gs-group-messages-topic-title cite").attr("id");c=GSStickyTopicToggle(b,d,a);
c.init()});