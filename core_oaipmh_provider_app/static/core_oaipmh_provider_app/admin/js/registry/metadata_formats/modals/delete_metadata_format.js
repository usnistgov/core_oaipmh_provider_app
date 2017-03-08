openDeleteMetadataFormatModal = function(event)
{
    event.preventDefault();

    var $metadataFormatRow = $(this).parent().parent();
    var objectID = $metadataFormatRow.attr("objectid");
    var metadataFormatName = $metadataFormatRow.find("td:first").text();

    $(".delete-metadata_format-name").text(metadataFormatName);
    $(".delete-metadata_format-type").text(event.data.name);
    $("#delete-metadata_format-id").val(objectID);
    $("#delete-metadata_format-modal").modal("show");
}

delete_metadata_format = function(event){
    event.preventDefault();
    type_ = $("#add-metadata_format-type").val();

    $.ajax({
        url : deleteMetadataFormatGetUrl,
        type : "GET",
        data: {
            "id": $("#delete-metadata_format-id").val()
        },
        success: function(data){
            location.reload();
        }
    });
}

$(document).on("click", ".delete-metadata_format-btn", { name: "Metadata Format"}, openDeleteMetadataFormatModal);
$(document).on("click", ".delete-template-metadata_format-btn", { name: "Template Metadata Format"}, openDeleteMetadataFormatModal);
$(document).on("click", "#delete-metadata_format-yes", delete_metadata_format);