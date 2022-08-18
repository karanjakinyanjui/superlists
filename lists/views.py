from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from lists.models import Item, List


def view_list(request, list_id):
    error = None
    if request.method == 'POST':
        item = Item.objects.create(text=request.POST['text'], list_id=list_id)
        try:
            item.full_clean()
        except ValidationError:
            item.delete()
            error = "You can't have an empty list item"
    item_list = List.objects.get(id=list_id)
    context = {"list": item_list, "error": error}
    return render(request, "lists/list.html", context=context)


def home_page(request):
    if request.method == 'POST':
        return new_list(request)
    return render(request, "lists/home.html")


def new_list(request):
    item_list = List.objects.create()
    item = Item.objects.create(text=request.POST['text'], list=item_list)
    try:
        item.full_clean()
    except ValidationError:
        item_list.delete()
        error = "You can't have an empty list item"
        return render(request, "lists/home.html", {"error": error})
    return redirect(item_list)
