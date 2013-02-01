// GroupServer module for supporting multi-file uploads.
jQuery.noConflict();
GSFileUpload = function (formId, widgetId, listId) {
    var remove = '<abbr class="muted" title="Remove this file from the list ' +
                 'of files">(remove)</abbr>';
    // Private methods
    var renameFileInputs = function(event) {
        var multiFiles = jQuery('.MultiFile-applied');
        var oldId = ''
        var newId = ''
        var i = null;
        var input = null;
        for ( i=0; i < multiFiles.length; i++ ) {
            input = jQuery(multiFiles[i]);
            oldId = input.attr('id');
            newId = oldId + '.' + i;
            input.attr('id', newId).attr('name', newId);
        }
        return true;
      };
    var addMultiFile = function () {
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

jQuery(document).ready( function () {
    var uploader = GSFileUpload('#add-to-topic', '#form\\.uploadedFile',
                                '#gs-group-messages-topic-add-file-files-list');
    uploader.init();
});
