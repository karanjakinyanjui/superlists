from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from lists.forms import ItemForm, ExistingListItemForm
from lists.models import Item, List


def view_list(request, list_id):
    item_list = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=item_list)
    if request.method == 'POST':
        form = ExistingListItemForm(request.POST, for_list=item_list)
        if form.is_valid():
            form.save(item_list)
            return redirect(item_list)
    context = {"list": item_list, "form": form}
    return render(request, "lists/list.html", context=context)


def home_page(request):
    if request.method == 'POST':
        return new_list(request)
    return render(request, "lists/home.html", {"form": ItemForm()})


def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        item_list = List.objects.create()
        form.save(item_list)
        return redirect(item_list)
    return render(request, "lists/home.html", {"form": form})
