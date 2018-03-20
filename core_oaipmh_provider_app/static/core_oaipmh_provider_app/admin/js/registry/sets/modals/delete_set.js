openDeleteSetModal = function(event)
{
    event.preventDefault();

    var $setRow = $(this).parent().parent().parent();
    var objectID = $setRow.attr("objectid");
    var setName = $setRow.find("td:first").text();

    $(".delete-set-name").text(setName);
    $("#delete-set-id").val(objectID);
    $("#delete-set-modal").modal("show");
}

delete_set = function(event){
    event.preventDefault();
    type_ = $("#add-set-type").val();

    $.ajax({
        url : deleteSetGetUrl,
        type : "GET",
        data: {
            "id": $("#delete-set-id").val()
        },
        success: function(data){
            location.reload();
        }
    });
}

$(document).on("click", ".delete-set-btn", openDeleteSetModal);
$(document).on("click", "#delete-set-yes", delete_set);