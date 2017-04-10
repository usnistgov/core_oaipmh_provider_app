/**
 * Opens template mapping modal.
 */
var openAddTemplateMappingModal = function(event) {
    event.preventDefault();

    clearAddError();
    $("#add-template_mapping-modal").modal("show");
}

/**
 * Clears errors.
 */
clearAddError = function ()
{
    $("#banner_add_errors").hide();
    $("#add-template_mapping-errors").html("");
}


/**
 * AJAX call. Adds the mapping.
 */
var saveTemplateMapping = function(event) {
   clearAddError();
   $("#banner_add_wait").show(200);
   var formData = new FormData($("#add-template_mapping-form")[0]);
   $.ajax({
        url: addTemplateMappingPostUrl,
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

$(document).on("click", ".add-template_mapping-btn", openAddTemplateMappingModal);
$(document).on("click", "#add-template_mapping-save", saveTemplateMapping);