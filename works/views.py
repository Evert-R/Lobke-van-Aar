from django.shortcuts import render
from works.models import work_items, work_images, categories
from works.forms import FilterForm
import math
# Create your views here.


def all_works(request):
    works = work_items.objects.filter(
        work_item=True).order_by('sort_order', 'id')
    filter_form = FilterForm()
    if request.method == "POST":
        filter_method = FilterForm(request.POST)
        if filter_method.is_valid():
            try:
                filter_results = filter_method.cleaned_data['cat'].id
            except:
                return render(request, "works.html", {"works": works,
                                                      "filter_form": filter_form})
            # Set this category as initial value for the form
            filter_form.fields['cat'].initial = filter_results
            works = works.filter(
                category=filter_results)
            return render(request, "works.html", {"works": works,
                                                  "filter_form": filter_form})
    else:
        """
        Because bootstrap orders card columns from top to bottom
        we create a new list that orders them horizontally
        """
        view_works = []
        # Get the total works count
        total = works.count()
        # Calculate how many rows we would get
        rows = int(math.ceil(total / 3))
        # Order the horizontally per row
        for iterator in range(rows):
            try:
                view_works.append(works[iterator])
            except:
                pass
            try:
                view_works.append(works[iterator+rows])
            except:
                pass
            try:
                view_works.append(works[iterator+(rows*2)])
            except:
                pass
        return render(request, "works.html", {"works": view_works,
                                              "filter_form": filter_form})


def work_details(request, pk):
    """ 
    Display a works details 
    and an overview of all works beneath
    """
    next = request.GET.get('next', '/')
    work = work_items.objects.get(pk=pk)
    images = work_images.objects.filter(
        work_item_id=pk).order_by('sort_order', 'id')
    works = work_items.objects.filter(
        work_item=True).order_by('sort_order', 'id')
    if work.collection == True:
        return render(request, "collection.html", {"work": work,
                                                   "images": images,
                                                   "works": works,
                                                   "next": next})
    else:
        return render(request, "workdetails.html", {"work": work,
                                                    "images": images,
                                                    "works": works,
                                                    "next": next})
