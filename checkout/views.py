from django.shortcuts import render, get_object_or_404, reverse, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .forms import PaymentForm, shippingForm
from .models import orders, order_items
from works.models import work_items
from shop.models import shipping
from accounts.models import user_details
from accounts.forms import UserDetailsForm
from django.conf import settings
from django.utils import timezone
import json, os, stripe
import uuid
# Create your views here.



@require_POST
@csrf_exempt
@login_required(login_url='accounts:register_user')
def create_payment(request):
    """
    Called when the page has loaded
    Creates the payment intent for stripe 
    """
    # Get cart contents
    cart = request.session.get('cart', {})
    total = 0
    # Return to shop if cart is empty
    if cart == {}:
        messages.error(
                request, 'There is nothing to check out')
        return redirect('shop:all_shop_works')
    # Get logged in user
    active_user = request.user
    try:
        current_user_details = user_details.objects.get(user=active_user)
    except:
        # If not show shipping details form
        messages.error(request, "Please provide your shipping details")
        return redirect('accounts:shipping_details')
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
    stripe_total = total * 100
    stripe.api_key = os.getenv('STRIPE_SECRET')
    		        
    # Create a PaymentIntent with the order amount and currency
    intent = stripe.PaymentIntent.create(
        amount=int(stripe_total),
        currency='eur',
        payment_method_types=['card', 'ideal'],            
        )
    try:
        return JsonResponse({'publishableKey':	
            os.getenv('STRIPE_PUBLISHABLE'), 'clientSecret': intent.client_secret})
    except Exception as e:
        return JsonResponse({'error':str(e)},status= 403)

@login_required()
@require_POST
def cache_checkout_data(request):
    """
    Called when the user clicks pay
    Creates the order object with shipping details
    and ordered items 
    """
    pid = request.POST.get('client_secret').split('_secret')[0]
    order_number = request.POST['order_number']
    full_name = request.POST['full_name']
    address1 = request.POST['address1']
    address2 = request.POST['address2']
    postcode = request.POST['postcode']
    city = request.POST['city']
    country = request.POST['country']
    telephone = request.POST['telephone']
    shipping = request.POST['shipping']
    order_message = request.POST['order_message']
    save_details = request.POST['save_details']
    # Get cart contents
    cart = request.session.get('cart', {})
    total = 0
    # Get logged in user
    active_user = request.user
    current_user_details = user_details.objects.get(user=active_user)
    if save_details == 'update':
        current_user_details.address1 = address1
        current_user_details.address2 = address2
        current_user_details.postcode = postcode
        current_user_details.city = city
        current_user_details.country = country
        current_user_details.telephone = telephone
        current_user_details.save()
    try:        
        stripe.api_key = os.getenv('STRIPE_SECRET')        
        stripe.PaymentIntent.modify(pid, metadata={
            'order_number': request.POST['order_number'],
            'full_name': request.POST['full_name'],
            'address1': request.POST['address1'],
            'address2': request.POST['address2'],
            'postcode': request.POST['postcode'],
            'city': request.POST['city'],
            'country': request.POST['country'],
            'telephone': request.POST['telephone'],
            'order_message': request.POST['order_message']
        })
        print(stripe.PaymentIntent)        
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)
    try:
        order = orders.objects.get(stripe_pid=stripe_pid)
        order.shipping = current_user_details.shipping.price
        order.region = current_user_details.shipping.region
        order.full_name = full_name
        order.address1 = address1
        order.address2 = address2
        order.postcode = postcode
        order.city = city
        order.country = country
        order.telephone = telephone
        order.order_message = order_message
        order.save()
    except:        
        order=orders(order_number=order_number,
                            stripe_pid=pid,
                            user=active_user,
                            date=timezone.now(),
                            shipping=current_user_details.shipping.price,
                            region=current_user_details.shipping.region,
                            full_name=full_name,
                            address1=address1,
                            address2=address2,
                            postcode=postcode,
                            city=city,
                            country=country,
                            telephone=telephone,
                            order_message=order_message
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
    order.total = total
    order.save()
    if save_details == 'update':
        current_user_details.address1 = address1
        current_user_details.address2 = address2
        current_user_details.postcode = postcode
        current_user_details.city = city
        current_user_details.country = country
        current_user_details.telephone = telephone
        current_user_details.save()
    return HttpResponse(status=200)
    




@csrf_exempt
@login_required(login_url='accounts:register_user')
def payment_complete(request):
    """
    Called when the payment was successfull
    Renders the payment complete page
    """
    try:        
        stripe_pid = request.GET['payment_intent']
        success = request.GET['redirect_status']
        pay_method = request.GET['pay_method']
    except:                
        messages.error(request, "There has been an error, please try again")
        return redirect('checkout:check_out')
    try:
        order = orders.objects.get(stripe_pid = stripe_pid)
    except:        
        messages.error(request, "There has been an error, please try again")
        return redirect('checkout:check_out')
    if success != 'succeeded':
        messages.error(request, "The payment was not successfull, please try again")
        order.delete()
        return redirect('checkout:check_out')

    # Get cart contents
    cart = request.session.get('cart', {})
    messages.success(request, "You have successfully paid")
    order.paid = True
    order.pay_method = pay_method
    order.save()
    ordered_items = order_items.objects.filter(order=order)
    # Adjust the stock for sold items
    for id, quantity in cart.items():
        work = get_object_or_404(work_items, pk=id)
        work.shop_settings.stock -= quantity
        work.shop_settings.save()
    request.session['cart'] = {}
    try:
        send_mail(
            'Thank you for your order',
            'I will prepare the package with the greatest care and sent you an e-mail with the tracking code when I have shipped it. If there is anything you would want to change or inform me about, please do not hesitate to send me an email.',
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
                       

    return render(request, "paymentcomplete.html",  
                    {'order': order,
                     'ordered_items': ordered_items})

@login_required(login_url='accounts:register_user')
def check_out(request):
    """
    Renders the checkout page with cart contents
    """
    next = request.GET.get('next', '/')
    # Get logged in user
    active_user = request.user
    try:
        current_user_details = user_details.objects.get(user=active_user)
    except:
        # If not show shipping details form
        messages.error(request, "Please provide your shipping details")
        return redirect('accounts:shipping_details')
    shipping_form = shippingForm()               
    # Get cart contents
    cart = request.session.get('cart', {})
    total = 0
    # Return to shop if cart is empty
    if cart == {}:
        messages.error(
                request, 'There is nothing to check out')
        return redirect('shop:all_shop_works')
    for id, quantity in cart.items():
            # Get work object
            work = get_object_or_404(work_items, pk=id)
            # Check if there is a discount
            if work.shop_settings.on_sale == True:
                price = work.shop_settings.discount_price
            else:
                price = work.shop_settings.price
            total += quantity * price
    if not request.user.is_authenticated:
        messages.error(request, "Please register before checking out")
        return redirect('accounts:register_user')
    order_unique = False
    order_number = ''
    while order_unique == False:
        order_number = uuid.uuid4().hex.upper()
        try:
            order = Order.objects.get(
                order_number=order_number
            )            
        except:
            order_unique = True
    if request.method == "POST":
        new_shipping = shippingForm(request.POST)
        if new_shipping.is_valid():
            shipping_id = new_shipping.cleaned_data['shipping_options'].id
            shipping_object = shipping.objects.get(id=shipping_id)
            current_user_details.shipping = shipping_object
            current_user_details.save()
            shipping_form.fields['shipping_options'].initial = current_user_details.shipping
        return render(request, "checkout.html",
            {'order_number': order_number,
            'total': total,
            'user': active_user,
            'user_details': current_user_details,
            'shipping_form': shipping_form,                                    
            'publishable': os.getenv('STRIPE_PUBLISHABLE'),
            'next': next})
    else:
        shipping_form.fields['shipping_options'].initial = current_user_details.shipping
        return render(request, "checkout.html",
                    {'order_number': order_number,
                    'total': total,
                    'user': active_user,
                    'user_details': current_user_details,
                    'shipping_form': shipping_form,                                    
                    'publishable': os.getenv('STRIPE_PUBLISHABLE'),
                    'next': next})
