from django.shortcuts import render, redirect

from lists.models import Item


def home_page(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['text'])
        return redirect('/')
    context = {"items": Item.objects.all()}
    return render(request, "lists/home.html", context=context)
