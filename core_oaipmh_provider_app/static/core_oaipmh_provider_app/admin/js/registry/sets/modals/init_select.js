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