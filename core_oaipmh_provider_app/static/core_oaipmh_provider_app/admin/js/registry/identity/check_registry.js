/**
 * Check the availability of a registry
 */
checkStatus = function()
{
    let $registryTd = $("#Status");
    let url = $registryTd.attr("url");

    $registryTd.html('<i class="fa fa-spinner fa-spin"></i>');

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
                $registryTd.html('<i class="fa fa-signal"></i> Available');
                $registryTd.css("color", "#5cb85c");
            }
            else {
                $registryTd.html('<i class="fa fa-signal"></i> Unavailable');
                $registryTd.css("color", "#d9534f");
            }
        },
        error:function(data){
            $registryTd.html('<i class="fa fa-warning"></i> '+data.responseText);
            $registryTd.css("color", "#d9534f");
        },
    });
};


$(document).ready(function() {
    $('.check-status-btn').on('click', checkStatus);
});