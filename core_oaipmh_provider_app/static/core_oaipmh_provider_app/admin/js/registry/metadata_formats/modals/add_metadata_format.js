var openAddMetadataFormatModal = function(event) {
    event.preventDefault();

    $(".add-metadata_format-name").text(event.data.name);
    $("#add-metadata_format-type").val(event.data.type);
    $("#add-metadata_format-modal").modal("show");

    load_add_metadata_format_form(event.data.type);
}

load_add_metadata_format_form = function(type_){
	$.ajax({
        url : getUrlFromType(type_),
        type : "GET",
        dataType: "json",
        success: function(data){
            $("#add-metadata_format-modal-form").html(data.template);
        }
    });
}

clearAddError = function ()
{
    $("#banner_add_errors").hide();
    $("#add-metadata_format-errors").html("");
}

validateMetadataFormat = function(type_)
{
    errors = ""
    if(type_ == metadata_format)
    {
        if ($( "#id_metadata_prefix" ).val().trim() == ""){
            errors += "<li>Please enter a metadata prefix.</li>"
        }
        if ($( "#id_schema" ).val().trim() == ""){
            errors += "<li>Please enter a schema.</li>"
        }
    }
    else if (type_ == template_metadata_format)
    {
        if ($( "#id_metadata_prefix" ).val().trim() == ""){
            errors += "<li>Please enter a metadata prefix.</li>"
        }
    }

	if (errors != ""){
	    error = "<ul>";
	    error += errors
	    error += "</ul>";
		$("#form_add_errors").html(errors);
		$("#banner_add_errors").show(200)
		return false;
	}

    return true;
}

addMetadataFormat = function(event) {
    clearAddError();
    type_ = $("#add-metadata_format-type").val();

    if(validateMetadataFormat(type_))
    {
       $("#banner_add_wait").show(200);
       var formData = new FormData($("#add-metadata_format-form")[0]);
       $.ajax({
            url: getUrlFromType(type_),
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
                $("#banner_add_wait").hide(200);
                $("#form_add_errors").html(data.responseText);
                $("#banner_add_errors").show(200)
            },
        })
        ;
    }
}

getUrlFromType = function(type_)
{
    var url = null;
    if(type_ == metadata_format)
        url = addMetadataFormatGetPostUrl;
    else if (type_ == template_metadata_format)
        url = addTemplateMetadataFormatGetPostUrl;

    return url;
}

$(document).on("click", ".add-metadata_format-btn", { name: "Metadata Format", type: metadata_format}, openAddMetadataFormatModal);
$(document).on("click", ".add-template-metadata_format-btn", { name: "Template Metadata Format", type: template_metadata_format}, openAddMetadataFormatModal);

