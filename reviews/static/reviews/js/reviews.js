/**
 * Sort reviews by rating and product name
 */
$('#sort-selector').change(function() {
    var selector = $(this);
    var currentUrl = new URL(window.location);

    var selectedVal = selector.val();
    var sort = selectedVal.split('_')[0];
    var direction = selectedVal.split('_')[1];

    if (selectedVal != 'reset') {
        currentUrl.searchParams.set("sort", sort);
        currentUrl.searchParams.set("direction", direction);

        window.location.replace(currentUrl);
    }
    else {
        currentUrl.searchParams.delete('sort', sort);
        currentUrl.searchParams.delete('direction', direction);

        window.location.replace(currentUrl);
    }
});