from django.shortcuts import render


def home_page(request):
    context = {"items": []}
    if request.method == 'POST':
        context['items'].append({"text": request.POST['text']})
    return render(request, "lists/home.html", context=context)
