from django.shortcuts import render, redirect, reverse,  get_object_or_404
from django.http import HttpRequest
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from accounts.models import user_details
from checkout.models import orders, order_items
from accounts.forms import LogInForm, RegisterForm, UserDetailsForm, UserUpdateForm
from accounts import decorators

# Create your views here.


@login_required
def user_profile(request):
    """Display profile page"""
    next = request.GET.get('next', '/')
    # Get active user
    active_user = request.user
    user_form = UserUpdateForm(instance=active_user)
    # Check if details already exist
    try:
        # If so create form with details
        current_user_details = user_details.objects.get(user=active_user)
        details_form = UserDetailsForm(instance=current_user_details)
    except:
        # If not create empty form
        details_form = UserDetailsForm({'user': active_user.id})
        current_user_details = None

     # Check if this order exists
    try:
        user_orders = orders.objects.filter(user=active_user).order_by('-date')

    # if not show the list and rais an error message
    except:
        user_orders = None

    ordered_items = order_items.objects.all()

    return render(request, 'profile.html',
                  {'active_user': active_user,
                   'user_details': current_user_details,
                   'user_form': user_form,
                   'details_form': details_form,
                   'orders': user_orders,
                   'ordered_items': ordered_items,
                   'title': 'Profile for ' + active_user.first_name + ' ' + active_user.last_name,
                   'next': next
                   })

@login_required
def view_order(request, order_number):
    """
    Renders user order view page
    """
    try:
        next = request.GET.get('next', '/')
    except:
        next = 'accounts:profile'
    # Get active user
    active_user = request.user
    try:
        print(order_number)
        order = orders.objects.get(order_number=order_number)
        
    except:        
        messages.error(request, "This order does not exist")
        return redirect(next)
    if order.user != active_user:
        messages.error(request, "You are not allowed to view this order")
        return redirect(next)
    ordered_items = order_items.objects.filter(order=order)
    return render(request, 'userorder.html',
                  {'order': order,
                  'ordered_items': ordered_items,
                  'next': next
                  })


@login_required
def update_user(request):
    """Register new users"""
    active_user = request.user
    # check if a form was submitted
    if request.method == 'POST':
        next = request.POST.get('next', '/')
        user_form = UserUpdateForm(request.POST, instance=active_user)
        if user_form.is_valid():
            user = user_form.save()
    else:
        return redirect('accounts:profile')
    return redirect(next)


def register_user(request):
    """Register new users"""
    # Get request origin to pass to the form
    next = request.GET.get('next', '/')
    accounts_form = RegisterForm()
    # check if a form was submitted
    if request.method == 'POST':
            # Get request origin from form
        next = request.POST.get('next', '/')
        # Create form object with submitted data
        accounts_form = RegisterForm(request.POST)
        if accounts_form.is_valid():
            # when valid save user to the database
            user = accounts_form.save()
            username = accounts_form.cleaned_data.get('username')
            # Add user to the customer group
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            # Display success message
            auth.login(user=user, request=request)
            messages.success(
                request, 'You are now registered and logged in as ' + username)
            # Return to request origin
            return redirect(next)
    # Show the register page
    return render(request, 'register.html',
                  {'accounts_form': accounts_form,
                   'next': next,
                   'title': 'Please register to use the webshop'})


@login_required
def add_user_details(request, next):
    """Add or edit user details"""
    # Check if next was provided as variable
    if next == None:
        # If not get request origin
        next = request.GET.get('next', '/')    
    # Get active user
    active_user = request.user
    # Check if details already exist
    try:
        # If so create form with details
        current_user_details = user_details.objects.get(user=active_user)
        accounts_form = UserDetailsForm(instance=current_user_details)
    except:
        # If not create empty form
        accounts_form = UserDetailsForm({'user': active_user.id})
        current_user_details = None
    # Check if a form was submitted
    if request.method == 'POST':
        # Get request origin from form
        next = request.POST.get('next', '/')
        # If so get the posted form
        accounts_form = UserDetailsForm(
            request.POST, instance=current_user_details)
        if accounts_form.is_valid():
            # Save data to the database
            current_user_details = accounts_form.save()
            messages.success(request, 'Your details have been saved')
            # return to origin
            return redirect(next)
    return render(request, 'userdetails.html',
                  {'accounts_form': accounts_form,
                   'next': next,
                   'title': 'Please provide your shipping details'})


def log_in(request):
    """Show login page"""
    # Get request origin
    next = request.GET.get('next', '/')
    accounts_form = LogInForm()
    if request.user.is_authenticated:
        messages.error(request, 'You are already logged in !')
        return redirect(reverse('all_works'))
    # check if a form was submitted
    if request.method == 'POST':
        # Get request origin from form
        next = request.POST.get('next', '/')
        # Create form object with submitted data
        accounts_form = LogInForm(request.POST)
        if accounts_form.is_valid():
            # when valid authenticate the user
            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password'])
            if user is not None:
                # When a user is matched log in
                auth.login(user=user, request=request)
                # Display success message
                messages.success(request, "You are now logged in!")
                # redirect to request origin
                return redirect(next)
            else:
                # When user was not matched return the form with errors
                accounts_form.add_error(
                    None, "Your username or password is incorrect")
    # Show the login page
    return render(request, 'login.html',
                  {'accounts_form': accounts_form,
                   'title': 'Please login to use the webshop',
                   'next': next})


@login_required
def log_out(request):
    """Log out user"""
    # Get request origin
    next = request.GET.get('next', '/')
    # Log user out
    auth.logout(request)
    messages.success(request, "You are now logged out!")
    # return to request origin
    return redirect(next)
