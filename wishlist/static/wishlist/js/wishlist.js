// Add/Remove products from wishlist
$('.btn-wishlist-heart').click(function(e) {
    e.preventDefault();
    var csrfToken = "{{ csrf_token }}";
    var productId = $(this).data('product-id')
    var url = `/wishlist/add/${productId}/`;
    var data = {'csrfmiddlewaretoken': csrfToken, 'product_id': productId};

    $.post(url, data)
        .done(function() {
            location.reload();
        });
})