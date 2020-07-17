from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import auth, messages
# Create your views here.


def view_cart(request):
    next = request.GET.get('next', '/')
    cart = request.session.get('cart', {})
    if cart == {}:
        messages.error(
                request, 'Your shopping cart is empty')
        return redirect('shop:all_shop_works')
    return render(request, "cart.html", {'next': next})


def add_cart(request, id):
    next = request.GET.get('next', '/')
    cart = request.session.get('cart', {})

    if id in cart:
        cart[id] = int(cart[id]) + 1
    else:
        cart[id] = cart.get(id, 1)

    request.session['cart'] = cart

    return redirect(next)


def remove_cart(request, id):
    next = request.GET.get('next', '/')
    cart = request.session.get('cart', {})

    cart[id] = int(cart[id]) - 1
    if cart[id] == 0:
        del request.session['cart'][id]
        request.session.modified = True

    request.session['cart'] = cart

    return redirect(next)
