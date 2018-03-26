InitSelectMultipleTemplates = function(path_elt)
{
    $(path_elt).fSelect({
        placeholder: 'Select templates',
        numDisplayed: 500,
        overflowText: '{n} selected',
        searchText: 'Search',
        showSearch: true
    });
}

$('#edit-object-modal').on('show.bs.modal error.bs.modal', function (e) {
    InitSelectMultipleTemplates("#edit-object-modal #id_templates_manager");
})


$('#add-object-modal').on('show.bs.modal error.bs.modal', function (e) {
    InitSelectMultipleTemplates("#add-object-modal #id_templates_manager");
})
