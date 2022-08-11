from django.shortcuts import render, redirect

from lists.models import Item


def home_page(request):
    return render(request, "lists/home.html")


def view_list(request):
    context = {"items": Item.objects.all()}
    return render(request, "lists/list.html", context=context)


def new_list(request):
    Item.objects.create(text=request.POST['text'])
    return redirect('/lists/the-only-list-in-the-world/')
