from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from .forms import PaymentForm
from .models import orders, order_items
from works.models import work_items
from accounts.models import user_details
from accounts.forms import UserDetailsForm
from django.conf import settings
from django.utils import timezone

import stripe

# Create your views here.

stripe.api_key = settings.STRIPE_SECRET


@login_required(login_url='accounts:register_user')
def check_out(request):
    next = request.GET.get('next', '/')
    # Get cart contents
    cart = request.session.get('cart', {})
    total = 0
    # Return to shop if cart is empty
    if cart == {}:
        messages.error(
                request, 'There is nothing to check out')
        return redirect('shop:all_shop_works')
    if not request.user.is_authenticated:
        messages.error(request, "Please register before checking out")
        return redirect('accounts:register_user')
    # Get logged in user
    active_user = request.user

    try:
        current_user_details = user_details.objects.get(user=active_user)
    except:
        # If not show shipping details form
        messages.error(request, "Please provide your shipping details")
        return redirect('accounts:shipping_details')
    # Attach user details to form
    accounts_form = UserDetailsForm(instance=current_user_details)
    # Check if a form was submitted
    if request.method == "POST":
        # Get both forms
        accounts_form = UserDetailsForm(
            request.POST, instance=current_user_details)
        payment_form = PaymentForm(request.POST)
        # If shipping details were changed update and return
        if accounts_form.is_valid():
            current_user_details = accounts_form.save()
            messages.success(request, 'Updated shipping details')
            return redirect('checkout:check_out')
        # if payment form is valid create order
        if payment_form.is_valid():
            order = orders(user=active_user,
                           date=timezone.now(),
                           shipping=current_user_details.shipping.price,
                           address1=current_user_details.address1,
                           address2=current_user_details.address2,
                           postcode=current_user_details.postcode,
                           city=current_user_details.city,
                           country=current_user_details.country,
                           telephone=current_user_details.telephone,
                           )
            order.save()
            # Add shipping cost to total
            total = current_user_details.shipping.price
            # Create order items for order
            for id, quantity in cart.items():
                work = get_object_or_404(work_items, pk=id)
                # Check if there is a discount
                if work.shop_settings.on_sale == True:
                    price = work.shop_settings.discount_price
                else:
                    price = work.shop_settings.price
                total += quantity * price
                order_item = order_items(
                    order=order,
                    work_item=work,
                    quantity=quantity,
                    price=price
                )
                order_item.save()
            # Make payment
            try:
                customer = stripe.Charge.create(
                    amount=int(total * 100),
                    currency="EUR",
                    description=request.user.email,
                    card=payment_form.cleaned_data['stripe_id'],
                )
            except stripe.error.CardError:
                messages.error(request, "Your card was declined!")

            if customer.paid:
                messages.error(request, "You have successfully paid")
                order.paid = True
                order.total = total
                order.save()
                # Adjust the stock for sold items
                for id, quantity in cart.items():
                    work = get_object_or_404(work_items, pk=id)
                    work.shop_settings.stock -= quantity
                    work.shop_settings.save()
                request.session['cart'] = {}
                try:
                    send_mail(
                        'Thank you for your order',
                        'I will prepare the package with the greatest care and sent you an e-mail with the tracking code when I shipped it. If there is anything you would want to change or inform me about, please do not hesitate to send me an email.',
                        'info@lobkevanaar.nl',
                        [active_user.email],
                        fail_silently=False,
                    )
                    send_mail(
                        'New order in the shop',
                        'A new order is waiting to be shipped.',
                        'info@lobkevanaar.nl',
                        ['evert.rot@gmx.com'],
                        fail_silently=False,
                    )
                except:
                    pass
                return redirect(reverse('shop:all_shop_works'))
            else:
                order.paid = False
                order.save()
                messages.error(request, "Unable to take payment")
        else:
            print(payment_form.errors)
            messages.error(
                request, "We were unable to take a payment with that card!")
    else:
        for id, quantity in cart.items():
            # Get work object
            work = get_object_or_404(work_items, pk=id)
            # Check if there is a discount
            if work.shop_settings.on_sale == True:
                price = work.shop_settings.discount_price
            else:
                price = work.shop_settings.price
            total += quantity * price
        payment_form = PaymentForm()
    return render(request, "checkout.html",
                  {'total': total,
                   'user': active_user,
                   'user_details': current_user_details,
                   'accounts_form': accounts_form,
                   'payment_form': payment_form,
                   'publishable': settings.STRIPE_PUBLISHABLE,
                   'next': next})
