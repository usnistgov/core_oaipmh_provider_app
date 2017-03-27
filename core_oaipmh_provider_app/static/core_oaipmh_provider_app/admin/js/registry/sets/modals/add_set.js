var openAddSetModal = function(event) {
    event.preventDefault();

    $("#add-set-modal").modal("show");
}

clearAddError = function ()
{
    $("#banner_add_errors").hide();
    $("#add-set-errors").html("");
}

validateSet = function()
{
    errors = ""
    if ($( "#add-set-form #id_set_spec" ).val().trim() == ""){
        errors += "<li>Please enter a set spec.</li>"
    }

    if ($( "#add-set-form #id_set_name" ).val().trim() == ""){
        errors += "<li>Please enter a set name.</li>"
    }

    if ($( "#add-set-form #id_description" ).val().trim() == ""){
        errors += "<li>Please enter a description.</li>"
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

var saveSet = function(event) {
    clearAddError();
    if(validateSet())
    {
       $("#banner_add_wait").show(200);
       var formData = new FormData($("#add-set-form")[0]);
       $.ajax({
            url: addSetPostUrl,
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

$(document).on("click", ".add-set-btn", openAddSetModal);
InitSelectMultipleTemplates("#add-set-form #id_templates_manager");