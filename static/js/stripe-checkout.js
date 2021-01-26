// A reference to Stripe.js
let stripe;

let orderData = {
    'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
};

// Get the payment intent from the local server
fetch("/checkout/create-payment-intent", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify(orderData)
})
    .then(function (result) {
        return result.json();
    })
    .then(function (data) {
        return setupElements(data);
    })
    .then(function ({ stripe, card, ideal, clientSecret }) {
        $('#client_secret').val(clientSecret);
        console.log(clientSecret);
        document.querySelector("#pay-form").addEventListener("submit", function (evt) {
            evt.preventDefault();
            // Initiate payment when the submit button is clicked
            pay(stripe, card, ideal, clientSecret);
        });
        document.querySelectorAll(".sr-pm-button").forEach(function (el) {
            el.addEventListener("click", function (evt) {
                let id = evt.target.id;
                if (id === "card-button") {
                    showElement("#card-element");
                    hideElement("#ideal-bank-element");
                    document.querySelector("#card-button").classList.add("selected");
                    document.querySelector("#ideal-button").classList.remove("selected");
                } else {
                    hideElement("#card-element");
                    showElement("#ideal-bank-element");
                    document.querySelector("#card-button").classList.remove("selected");
                    document.querySelector("#ideal-button").classList.add("selected");
                }
            });
        });
    });

// Set up Stripe.js and Elements to use in checkout form
let setupElements = function (data) {
    stripe = Stripe(data.publishableKey, { betas: ["ideal_pm_beta_1"] });
    let elements = stripe.elements();
    let style = {
        base: {
            color: "#32325d",
            fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
            fontSmoothing: "antialiased",
            fontSize: "16px",
            "::placeholder": {
                color: "#aab7c4"
            },
            padding: "10px 12px"
        },
        invalid: {
            color: "#fa755a",
            iconColor: "#fa755a"
        }
    };

    let card = elements.create("card", { style: style });
    card.mount("#card-element");

    let idealBank = elements.create("idealBank", { style: style });
    idealBank.mount("#ideal-bank-element");

    return {
        stripe: stripe,
        card: card,
        ideal: idealBank,
        clientSecret: data.clientSecret
    };
};

// Sent order info to local server to create the order
function cacheCheckoutData(clientSecret) {
    let postData = {
        'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
        'client_secret': clientSecret,
        'order_number': $('#order_number').val(),
        'address1': $('#address1').val(),
        'address2': $('#address2').val(),
        'postcode': $('#postcode').val(),
        'city': $('#city').val(),
        'country': $('#country').val(),
        'telephone': $('#telephone').val()
    }
    let url = '/checkout/cache-checkout-data';
    $.post(url, postData).done();
}

/*
 * Calls stripe.handleCardPayment which creates a pop-up modal to
 * prompt the user to enter extra authentication details without leaving your page
 */
let pay = function (stripe, card, ideal, clientSecret) {
    changeLoadingState(true);

    const selectedPaymentMethod = document.querySelector(
        ".sr-pm-button.selected"
    );

    let postData = {
        'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
        'client_secret': clientSecret,
        'order_number': $('#order_number').val(),
        'address1': $('#address1').val(),
        'address2': $('#address2').val(),
        'postcode': $('#postcode').val(),
        'city': $('#city').val(),
        'country': $('#country').val(),
        'telephone': $('#telephone').val()
    }

    let url = '/checkout/cache-checkout-data';
    $.post(url, postData).done(function () {
        switch (selectedPaymentMethod.id) {
            case "card-button":
                payWithCard(stripe, clientSecret, card, postData);
                return;
            case "ideal-button":
                payWithiDEAL(stripe, clientSecret, ideal, postData);
                return;
            default:
                console.log("Error: no payment method selected");
        }
    });
};

let payWithCard = function (stripe, clientSecret, card, postData) {
    // Initiate the payment.
    // If authentication is required, confirmCardPayment will automatically display a modal
    stripe
        .confirmCardPayment(clientSecret, { payment_method: { card: card } })
        .then(function (result) {
            if (result.error) {
                // Show error to your customer
                showError(result.error.message);
            } else {
                // The payment has been processed!
                orderComplete(clientSecret, postData);
            }
        });
};

let payWithiDEAL = function (stripe, clientSecret, ideal, postData) {
    // Initiate the payment.
    // confirmIdealPayment will redirect the customer to their bank
    stripe
        .confirmIdealPayment(clientSecret, {
            payment_method: {
                ideal: ideal
            },
            return_url: `http://${window.location.hostname}/checkout/payment-complete?pay_method=ideal`
        })
};

/* ------- Post-payment helpers ------- */

/* Shows a success / error message when the payment is complete */
let orderComplete = function (clientSecret, postData) {
    stripe.retrievePaymentIntent(clientSecret).then(function (result) {
        let paymentIntent = result.paymentIntent;
        let paymentIntentJson = JSON.stringify(paymentIntent, null, 2);
        console.log(paymentIntentJson);
        document.querySelector(".sr-payment-form").classList.add("hidden");
        document.querySelector(".sr-picker").classList.add("hidden");
        document.querySelector(".sr-result").classList.remove("hidden");

        changeLoadingState(false);
        window.location.href = `http://${window.location.hostname}/checkout/payment-complete?payment_intent=${paymentIntent.id}&pay_method=card&redirect_status=succeeded`
    });
};

let showError = function (errorMsgText) {
    changeLoadingState(false);
    let errorMsg = document.querySelector(".sr-field-error");
    errorMsg.textContent = errorMsgText;
    setTimeout(function () {
        errorMsg.textContent = "";
    }, 4000);
};

// Show a spinner on payment submission
let changeLoadingState = function (isLoading) {
    if (isLoading) {
        showElement("#spinner");
        hideElement("#button-text");
        document.querySelector("#submit").disabled = true;
    } else {
        hideElement("#spinner");
        showElement("#button-text");
        document.querySelector("#submit").disabled = false;
    }
};

let showElement = function (query) {
    document.querySelector(query).classList.remove("hidden");
};

let hideElement = function (query) {
    document.querySelector(query).classList.add("hidden");
};