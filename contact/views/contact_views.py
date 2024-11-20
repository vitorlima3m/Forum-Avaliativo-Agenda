from django.shortcuts import render, get_object_or_404,redirect
from django.db.models import Q
from contact.models import Contact
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

@login_required(login_url='contact:login') 
def index (request):
    # contacts= Contact.objects.all().filter(show=True).order_by('-id')
    #Mostra somente os contatos do usuario logado
    contacts= Contact.objects.filter(show=True, owner=request.user).order_by('-id')
    paginator = Paginator(contacts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'site_title': 'Contatos - '
    }
    
    return render(
        request,
        'contact/index.html',
        context
    )
    
def contact (request, contact_id):
    single_contact= get_object_or_404(Contact.objects, pk=contact_id, show=True)
    contact_name = f'{single_contact.first_name} {single_contact.last_name}'
    context = {
        'contact': single_contact,
        'site_title': contact_name
    }
    
    return render(
        request,
        'contact/contact.html',
        context
    )
    
def search (request):
    search_value = request.GET.get('q','').strip()
    if search_value == '':
        return redirect('contact:index')
    
    contacts= Contact.objects.all()\
        .filter(show=True, owner=request.user)\
        .filter(
            Q(first_name__icontains=search_value) |
            Q(last_name__icontains=search_value) |
            Q(phone__icontains=search_value) |
            Q(email__icontains=search_value)
            )\
        .order_by('-id')
        
    paginator = Paginator(contacts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'site_title': 'Contatos - '
    }
    
    return render(
        request,
        'contact/index.html',
        context
    )