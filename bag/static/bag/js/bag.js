/**
 * Update quantity on click
 */
$('.update-link').click(function() {
    var form = $(this).prev('.update-form');
    form.submit();
});

/**
 * Remove item and reload on click
 */
$('.remove-item').click(function() {
    var csrfToken = "{{ csrf_token }}";
    var itemId = $(this).attr('id').split('remove_')[1];
    var size = $(this).data('product_size');
    var url = `/bag/remove/${itemId}/`;
    var data = {'csrfmiddlewaretoken': csrfToken, 'product_size': size};

    $.post(url, data)
        .done(function() {
            location.reload();
        });
});