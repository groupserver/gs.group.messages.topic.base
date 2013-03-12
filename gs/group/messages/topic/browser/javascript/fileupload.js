// GroupServer module for supporting multi-file uploads.
jQuery.noConflict();
function GSFileUpload(formId, widgetId, listId) {
    var remove = '<abbr class="muted" title="Remove this file from the list ' +
                 'of files">(remove)</abbr>';
    // Private methods
    function renameFileInputs(event) {
        var multiFiles = jQuery('.MultiFile-applied'), oldId = '', newId = '',
        i = null, input = null;
        for ( i=0; i < multiFiles.length; i++ ) {
            input = jQuery(multiFiles[i]);
            oldId = input.attr('id');
            newId = oldId + '.' + i;
            input.attr('id', newId).attr('name', newId);
        }
        return true;
    };

    // Public methods and properties
    return {
        init: function () {
            var options = {
                list: listId,
                STRING: {remove: remove}
            };
            jQuery(widgetId).MultiFile(options);
            jQuery(formId).submit(renameFileInputs);
        }
    };
}; // GSFileUpload

function init_multifile() {
    var uploader = null;
    uploader = GSFileUpload('.gs-group-messages-topic-add', 
                            '#form\\.uploadedFile',
                            '.gs-group-messages-topic-add-file-files-list');
    uploader.init();
}

jQuery(window).load( function () {
    var url = '/++resource++multiple_file_upload-1.48/jquery.MultiFile.js';
    if (jQuery('.gs-group-messages-topic-add').length != 0) {
        gsJsLoader.with_module(url, init_multifile);
    }
});
