/**
 * Opens template mapping edit modal.
 */
var openEditMappingModal = function(event) {
    event.preventDefault();

    var $template_mappingRow = $(this).parent().parent();
    var objectID = $template_mappingRow.attr("objectid");
    var template_mappingName = $template_mappingRow.find("td:first").text();

    $(".edit-template_mapping-name").text(template_mappingName);
    $("#edit-template_mapping-modal").modal("show");

    load_edit_template_mapping_form(objectID);
}

/**
 * AJAX call. Loads the form.
 * @param objectID id of the object.
 */
load_edit_template_mapping_form = function(objectID){
	$.ajax({
        url : editMappingGetPostUrl,
        type : "GET",
        dataType: "json",
        data : {
            "id": objectID
        },
        success: function(data){
            $("#edit-template_mapping-modal-form").html(data.template);
        }
    });
}

/**
 * Clears errors.
 */
clearEditError = function ()
{
    $("#banner_edit_errors").hide()
    $("#form_edit_errors").html("");
}


/**
 * AJAX call. Edits the mapping.
 */
var editMapping = function(event) {
    clearEditError();
    var formData = new FormData($("#edit-template_mapping-form")[0]);
    $.ajax({
        url: editMappingGetPostUrl,
        type: 'POST',
        data: formData,
        cache: false,
        contentType: false,
        processData: false,
        async:true,
        success: function(data){
            location.reload();
        },
        error:function(data){
            $("#form_edit_errors").html(data.responseText);
            $("#banner_edit_errors").show(200)
        },
    })
    ;
}

$(document).on("click", ".edit-template_mapping-btn", openEditMappingModal);
$(document).on("click", "#edit-template_mapping-save", editMapping);