from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Item

def listOfItems(request):
    items=Item.objects.all().values()
    template=loader.get_template('list.html')
    context = {
        'myitems':items,
    }

    return HttpResponse(template.render(context, request))

def details(request, id):
  myitem = Item.objects.get(id=id)
  template = loader.get_template('details.html')
  context = {
    'myitem': myitem,
  }
  return HttpResponse(template.render(context, request))
# Create your views here.

def main(request):
  template = loader.get_template('main.html')
  return HttpResponse(template.render())
    
