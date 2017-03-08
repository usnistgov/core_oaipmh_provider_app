var openEditMetadataFormatModal = function(event) {
    event.preventDefault();

    var $metadataFormatRow = $(this).parent().parent();
    var objectID = $metadataFormatRow.attr("objectid");
    var metadataFormatName = $metadataFormatRow.find("td:first").text();

    $(".edit-metadata_format-name").text(metadataFormatName);
    $(".edit-metadata_format-type").text(event.data.name);
    $("#edit-metadata_format-modal").modal("show");

    load_edit_metadata_format_form(objectID);
}

load_edit_metadata_format_form = function(objectID){
	$.ajax({
        url : editMetadataFormatGetPostUrl,
        type : "GET",
        dataType: "json",
        data : {
            "id": objectID
        },
        success: function(data){
            $("#edit-metadata_format-modal-form").html(data.template);
        }
    });
}

clearEditError = function ()
{
    $("#banner_edit_errors").hide()
    $("#form_edit_errors").html("");
}

validateEditMetadataFormat = function()
{
    errors = ""
    if ($( "#edit-metadata_format-form #id_metadata_prefix" ).val().trim() == ""){
        errors += "<li>Please enter a metadata prefix.</li>"
    }
	if (errors != ""){
	    error = "<ul>";
	    error += errors
	    error += "</ul>";
		$("#form_edit_errors").html(errors);
		$("#banner_edit_errors").show(200)
		return (false);
	}else{
		return (true)
	}
    return true;
}

var editMetadataFormat = function(event) {
    clearEditError();
    if(validateEditMetadataFormat())
    {
       var formData = new FormData($("#edit-metadata_format-form")[0]);
       $.ajax({
            url: editMetadataFormatGetPostUrl,
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
}

$(document).on("click", ".edit-metadata_format-btn", { name: "Metadata Format"}, openEditMetadataFormatModal);
$(document).on("click", ".edit-template-metadata_format-btn", { name: "Template Metadata Format"}, openEditMetadataFormatModal);

