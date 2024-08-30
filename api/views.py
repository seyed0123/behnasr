import numpy as np
from PIL import Image
from io import BytesIO
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib import messages

from .forms import *
from .models import *
from base.models import Company
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes, api_view


# Create your views here.

def signup(request):
    lang = request.GET.get('lang', 'en')
    if lang not in [p[0] for p in language_choices]:
        lang = 'en'
    api_methods = ApiMethod.objects.filter(language=lang)
    company_obj = Company.objects.get(language=lang)
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form, 'company': company_obj, 'api_methods': api_methods})


def login(request):
    lang = request.GET.get('lang', 'en')
    if lang not in [p[0] for p in language_choices]:
        lang = 'en'
    api_methods = ApiMethod.objects.filter(language=lang)
    company_obj = Company.objects.get(language=lang)
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form, 'company': company_obj, 'api_methods': api_methods})


def logout_view(request):
    auth_logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    lang = request.GET.get('lang', 'en')
    if lang not in [p[0] for p in language_choices]:
        lang = 'en'
    company_obj = Company.objects.get(language=lang)
    api_methods = ApiMethod.objects.filter(language=lang)
    userAPI = UserAPI.objects.get(user=request.user)
    return render(request, 'profile.html', {'userAPI': userAPI, 'company': company_obj, 'api_methods': api_methods})


def convert_image_to_numpy_array(image_file):
    image = Image.open(image_file)

    image_array = np.array(image)

    return image_array


@csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def classify(request):
    user = request.user
    # Check if the image is in the request
    image = request.FILES.get('image')
    if not image:
        return JsonResponse({'error': 'No image provided.'}, status=400)
    image_array = convert_image_to_numpy_array(image)
    # Check if the method is in the request
    method = request.POST.get('method')
    if not method:
        return JsonResponse({'error': 'No method provided.'}, status=400)

    # TODO: parse the params and call the classify method and make a valid json response in the dict format
    res = {}

    userAPI = UserAPI.objects.get(user=user)
    if userAPI.tokens <= 0:
        return JsonResponse({'error': 'Insufficient tokens.'}, status=403)

    userAPI.tokens -= 1
    userAPI.save()
    # Process the image and method here
    # Example: save the image, perform an action based on the method, etc.

    # Example response after processing
    return JsonResponse({'success': True, **res},
                        status=200)


def method(request, pk):
    lang = request.GET.get('lang', 'en')
    if lang not in [p[0] for p in language_choices]:
        lang = 'en'
    api_method = get_object_or_404(ApiMethod, pk=pk)
    company_obj = Company.objects.get(language=lang)
    api_methods = ApiMethod.objects.filter(language=lang)
    return render(request, 'document.html',
                  {'company': company_obj, 'api_method': api_method, 'api_methods': api_methods})


def api_method_list(request):
    lang = request.GET.get('lang', 'en')
    if lang not in [p[0] for p in language_choices]:
        lang = 'en'
    company_obj = Company.objects.get(language=lang)
    api_methods = ApiMethod.objects.filter(language=lang)
    return render(request, 'api_list.html', {'company': company_obj, 'api_methods': api_methods})
