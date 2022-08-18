from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from lists.forms import ItemForm
from lists.models import Item, List


def view_list(request, list_id):
    form = ItemForm()
    if request.method == 'POST':
        post_form = ItemForm(request.POST)
        if post_form.is_valid():
            Item.objects.create(text=request.POST['text'], list_id=list_id)
        else:
            form = post_form
    item_list = List.objects.get(id=list_id)
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
        Item.objects.create(text=request.POST['text'], list=item_list)
        return redirect(item_list)
    return render(request, "lists/home.html", {"form": form})
