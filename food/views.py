from django.forms.models import BaseModelForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Item
from .forms import ItemForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    item_list = Item.objects.all()
    context = {
        'item_list': item_list,
    }
    return render(request, 'food/index.html', context)

class IndexClassView(ListView):
    model= Item
    template_name = 'food/index.html'
    context_object_name = 'item_list'

def item(request):
    return HttpResponse("this is item")

def detail(request, item_id):
    item = Item.objects.get(pk=item_id)
    context = {
        'item': item,
    }
    return render(request, 'food/detail.html', context)

class DetailClassView(DetailView):
    model = Item
    template_name = 'food/detail.html'

def create_item(request):
    form = ItemForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('food:index')
    
    return render(request, 'food/item-form.html', {'form':form})

class CreateItem(CreateView):
    model= Item
    fields = ['item_name', 'item_desc', 'item_price', 'item_image']
    template_name = 'food/item-form.html'

    def form_valid(self, form):
        form.instance.user_name = self.request.user
        return super().form_valid(form)

def update_item(request, id):
    item = Item.objects.get(id=id)
    form = ItemForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('food:index')
    
    return render(request, 'food/item-form.html', {'form':form, 'item':item})

def delete_item(request, id):
    item = Item.objects.get(id=id)
    if request.method == 'POST':
        item.delete()
        return redirect('food:index')
    
    return render(request, 'food/item-delete.html', {'item':item})

def item_list(request):
    item_objects = Item.objects.all()

    item_searched_name = request.GET.get('item_name')
    if item_searched_name != '' and item_searched_name is not None:
        item_objects = item_objects.filter(item_name__icontains=item_searched_name)

    paginator = Paginator(item_objects, 2)
    page = request.GET.get('page')
    item_objects = paginator.get_page(page)
    return render(request, 'food/item_list.html', {'item_objects': item_objects})