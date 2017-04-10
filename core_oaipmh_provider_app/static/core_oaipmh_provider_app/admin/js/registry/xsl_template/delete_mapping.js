/**
 * Opens template mapping delete modal.
 */
openDeleteMappingModal = function(event)
{
    event.preventDefault();

    var $setRow = $(this).parent().parent();
    var objectID = $setRow.attr("objectid");
    var setName = $setRow.find("td:first").text();

    $(".delete-template_mapping-name").text(setName);
    $("#delete-template_mapping-id").val(objectID);
    $("#delete-template_mapping-modal").modal("show");
}

/**
 * AJAX call. Deletes the mapping.
 */
delete_template_mapping = function(event){
    event.preventDefault();

    $.ajax({
        url : deleteMappingGetUrl,
        type : "GET",
        data: {
            "id": $("#delete-template_mapping-id").val()
        },
        success: function(data){
            location.reload();
        }
    });
}

$(document).on("click", ".delete-template_mapping-btn", openDeleteMappingModal);
$(document).on("click", "#delete-template_mapping-yes", delete_template_mapping);