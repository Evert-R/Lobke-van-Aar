from django.shortcuts import render
from works.models import work_items, work_images, categories
from shop.forms import ShopFilterForm
from .models import shop_message

# Create your views here.


def all_shop_works(request):
    """
    Show all works in the shop
    """
    # Only show shop message from the navbar link
    info = request.GET.get('info')
    # Get the shop message object
    try:
        message = shop_message.objects.first()
        # Show only if message is set to show
        if message.show == False:
            message = None
    except:
        message = None
        # Get all works for the shop
    works = work_items.objects.filter(
        shop_item=True).order_by('shop_settings__sort_order', 'id')
    shop_filter_form = ShopFilterForm()

    if request.method == "POST":
        title = 'all works'
        shop_filter = ShopFilterForm(request.POST)
        if shop_filter.is_valid():
            title = ''
            try:
                # Check if a work type was selected
                filter_type = shop_filter.cleaned_data['type'].id
                type_name = shop_filter.cleaned_data['type'].name
                # Set this type as initial value for the form
                shop_filter_form.fields['type'].initial = filter_type
                # Filter the works by type
                works = works.filter(shop_settings__work_type=filter_type)
                title += ' / ' + type_name
            except:
                type_name = ''
            try:
                filter_size = shop_filter.cleaned_data['size'].id
                size_name = shop_filter.cleaned_data['size'].name
                shop_filter_form.fields['size'].initial = filter_size
                works = works.filter(shop_settings__work_size=filter_size)
                title += ' / ' + size_name
            except:
                size_name = ''
            try:
                filter_mat = shop_filter.cleaned_data['mat'].id
                material_name = shop_filter.cleaned_data['mat'].name
                shop_filter_form.fields['mat'].initial = filter_mat
                works = works.filter(shop_settings__material=filter_mat)
                title += ' / ' + material_name
            except:
                filter_mat = ''
            return render(request, "shopworks.html", {"works": works,
                                                      "shop_filter_form": shop_filter_form,
                                                      'title': 'Viewing: ' + title})


    title = 'Viewing all works'
    return render(request, "shopworks.html", {"works": works,
                                              "shop_filter_form": shop_filter_form,
                                              "title": title,
                                              "message": message,
                                              "info": info})


def shop_details(request, pk):
    next = request.GET.get('next', '/')
    work = work_items.objects.get(pk=pk)
    images = work_images.objects.filter(
        work_item_id=pk).order_by('sort_order', 'id')
    return render(request, "shopdetails.html",
                  {"work": work,
                   "images": images,
                   "next": next})
