var openEditIdentityModal = function(event) {
    event.preventDefault();
    $("#edit-identity-modal").modal("show");

    load_edit_identity_form();
}

load_edit_identity_form = function(objectID){
	$.ajax({
        url : editIdentityGetPostUrl,
        type : "GET",
        dataType: "json",
        success: function(data){
            $("#edit-identity-modal-form").html(data.template);
        }
    });
}

clearEditError = function ()
{
    $("#banner_edit_errors").hide()
    $("#form_edit_errors").html("");
}

validateIdentity = function()
{
    errors = ""
    if ($( "#id_name" ).val().trim() == ""){
        errors += "<li>Please enter a name.</li>"
    }
    if ($( "#id_repository_identifier" ).val().trim() == ""){
        errors += "<li>Please enter a repository identifier.</li>"
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

var editIdentity = function(event) {
    clearEditError();
    if(validateIdentity())
    {
       var formData = new FormData($("#edit-identity-form")[0]);
       $.ajax({
            url: editIdentityGetPostUrl,
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

$(".edit-identity-btn").on('click', openEditIdentityModal);
