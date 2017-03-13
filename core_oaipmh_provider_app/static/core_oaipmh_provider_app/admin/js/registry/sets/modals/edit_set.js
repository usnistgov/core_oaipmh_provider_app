var openEditSetModal = function(event) {
    event.preventDefault();

    var $setRow = $(this).parent().parent();
    var objectID = $setRow.attr("objectid");
    var setName = $setRow.find("td:first").text();

    $(".edit-set-name").text(setName);
    $("#edit-set-modal").modal("show");

    load_edit_set_form(objectID);
}

load_edit_set_form = function(objectID){
	$.ajax({
        url : editSetGetPostUrl,
        type : "GET",
        dataType: "json",
        data : {
            "id": objectID
        },
        success: function(data){
            $("#edit-set-modal-form").html(data.template);
            InitSelectMultipleTemplates("#edit-set-form #id_templates");
        }
    });
}

clearEditError = function ()
{
    $("#banner_edit_errors").hide()
    $("#form_edit_errors").html("");
}

validateEditSet = function()
{
    errors = ""
    if ($( "#edit-set-form #id_set_spec" ).val().trim() == ""){
        errors += "<li>Please enter a set spec.</li>"
    }

    if ($( "#edit-set-form #id_set_name" ).val().trim() == ""){
        errors += "<li>Please enter a set name.</li>"
    }

    if ($( "#edit-set-form #id_description" ).val().trim() == ""){
        errors += "<li>Please enter a description.</li>"
    }

	if (errors != ""){
	    error = "<ul>";
	    error += errors
	    error += "</ul>";
		$("#form_edit_errors").html(errors);
		$("#banner_edit_errors").show(200)
		return false;
	}
    return true;
}

var editSet = function(event) {
    clearEditError();
    if(validateEditSet())
    {
       var formData = new FormData($("#edit-set-form")[0]);
       $.ajax({
            url: editSetGetPostUrl,
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

$(document).on("click", ".edit-set-btn", openEditSetModal);