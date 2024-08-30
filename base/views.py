from django.shortcuts import render, get_object_or_404

from api.models import ApiMethod
from .models import *


# Create your views here.
def index(request):
    lang = request.GET.get('lang', 'en')
    if lang not in [p[0] for p in language_choices]:
        lang = 'en'

    company_obj = Company.objects.get(language=lang)
    about_list = About_item.objects.filter(language=lang)
    services = Service.objects.filter(language=lang)
    products = Product.objects.filter(language=lang)
    categories = list(Product.objects.values('category').distinct())
    members = Member.objects.filter(language=lang)
    prices = Pricing.objects.filter(language=lang)
    customers = Customer.objects.all()
    api_methods = ApiMethod.objects.filter(language=lang)

    return render(request, 'index.html',
                  {'company': company_obj, 'about_list': about_list, 'services': services, 'products': products,
                   'categories': categories, 'members': members, 'prices': prices, 'customers': customers,
                   'api_methods': api_methods})


def view_product(request, pk=None):
    lang = request.GET.get('lang', 'en')
    if lang not in [p[0] for p in language_choices]:
        lang = 'en'
    product = get_object_or_404(Product, pk=pk)
    company_obj = Company.objects.get(language=lang)
    api_methods = ApiMethod.objects.filter(language=lang)

    return render(request, 'portfolio-details.html',
                  {'company': company_obj, 'product': product, 'api_methods': api_methods})
