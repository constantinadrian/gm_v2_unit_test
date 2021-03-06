/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment
    CSS from here: 
    https://stripe.com/docs/stripe-js
*/

var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
// Create a variable with the public stripe key 
var stripe = Stripe(stripePublicKey);
// Create an instance of stripe elements
var elements = stripe.elements();
// Custom style for when creating an Element
var style = {
    base: {
        color: '#000',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};
// Create a card element which also accepts an style argument 
var card = elements.create('card', {style: style});
// Mount the card element to div
card.mount('#card-element');


// Handle realtime validation errors on the card element
card.addEventListener('change', function (event) {
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {
        var html = `
                        <span class="icon" role="alert">
                            <i class="fas fa-times"></i>
                        </span>
                        <span>${event.error.message}</span>
                    `;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});


// Handle form submit
var form = document.getElementById('payment-form');

form.addEventListener('submit', function(ev) {
    ev.preventDefault();

    // before call out stripe disable both the card element and the
    // submit button to prevent multiple submissions
    card.update({ 'disabled': true});
    $('#submit-button').attr('disabled', true);
    $('#payment-form').fadeToggle(100);
    $('#loading-overlay').fadeToggle(100);

    // Create variable to make a post request to capture 
    // the form data we can't put in the payment intent here

    // get the value of save box
    var saveInfo = Boolean($('#id-save-info').attr('checked'));

    // get csrfToken
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    

    // create an object to pass the info
    var postData = {
        'csrfmiddlewaretoken': csrfToken,
        'client_secret': clientSecret,
        'save_info': saveInfo,
    };

    // create a variable for the url
    var url = '/checkout/cache_checkout_data/';

    // Post the data to the cache_checkout_data view
    // The view updates the payment intent
    $.post(url, postData).done(function(){
        // Call the confirmCardPayment method 
        stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card,
                billing_details: {
                    email: $.trim(form.email.value)
                }
            },
            shipping: {
                name: $.trim(form.full_name.value),
                phone: $.trim(form.phone_number.value),
                address: {
                    line1: $.trim(form.street_address1.value),
                    line2: $.trim(form.street_address2.value),
                    city: $.trim(form.town_or_city.value),
                    country: $.trim(form.country.value),
                    postal_code: $.trim(form.postcode.value),
                    state: $.trim(form.county.value),
                }
            },
        }).then(function(result) {
            if (result.error) {
                var errorDiv = document.getElementById('card-errors');
                var html = `
                                <span class="icon" role="alert">
                                    <i class="fas fa-times"></i>
                                </span>
                                <span>${result.error.message}</span>
                            `;
                $(errorDiv).html(html);

                $('#payment-form').fadeToggle(100);
                $('#loading-overlay').fadeToggle(100);

                card.update({ 'disabled': false});
                $('#submit-button').attr('disabled', false);
            } else {
                // The payment has been processed!
                if (result.paymentIntent.status === 'succeeded') {
                    form.submit();
                }
            }
        });
    }).fail(function() {
        // just reload the page to show the error from the view
        // the error will be in django messages
        location.reload();
    });
});