from django.shortcuts import render

# Create your views here.
def show_mountains(request):
    template_name = 'appmountain/index.html'
    data = {
        'title': 'НАЗВАНИЕ',
        'context': 'Горы'
    }
    return render(request, template_name=template_name, context=data)
