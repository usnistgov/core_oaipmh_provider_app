/**
 * Check the availability of a registry
 */
checkStatus = function()
{
    let $registryTd = $("#Status");
    let url = $registryTd.attr("url");

    $registryTd.html('<i class="fas fa-spinner fa-spin"></i>');

    $.ajax({
        url : checkRegistryGetUrl,
        type : "GET",
        dataType: "json",
        async: true,
        data : {
        	url : url,
        },
        success: function(data){
            if ("is_available" in data && data.is_available)
            {
                $registryTd.html('<i class="fas fa-signal"></i> Available');
                $registryTd.css("color", "#5cb85c");
            }
            else {
                $registryTd.html('<i class="fas fa-signal"></i> Unavailable');
                $registryTd.css("color", "#d9534f");
            }
        },
        error:function(data){
            $registryTd.html('<i class="fas fa-warning"></i> '+data.responseText);
            $registryTd.css("color", "#d9534f");
        },
    });
};


/**
 * Copy base url
 */
copyURL = function()
{
    // Create a temporary text field
    let $temp = $("<input>");
    $("body").append($temp);
    // Select the text field
    $temp.val($.trim($(".base-url").text())).select();
    // Copy the text inside the text field
    navigator.clipboard.writeText($temp.val()).then(function() {
        $.notify("Base URL copied to clipboard!", "success");
    }, function() {
        $.notify("An error has occurred while copying the base URL!", "danger");
    });

    // Remove a temporary text field
    $temp.remove();
}

$(document).ready(function() {
    $('.check-status-btn').on('click', checkStatus);
    $('.copy-base-url-btn').on('click', copyURL)
});