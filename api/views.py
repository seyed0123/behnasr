import io

import numpy as np
import requests
from PIL import Image
from io import BytesIO
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib import messages
from django.utils import translation

from apiwebsite import settings
from .forms import *
from .models import *
from base.models import Company
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes, api_view

flask_url = "http://localhost:5000"


def active_lang(req, html, content, lang):
    translation.activate(lang)
    response = render(req, html, content)
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang)
    return response


# Create your views here.

def signup(request):
    lang = translation.get_language()
    if lang not in [p[0] for p in language_choices]:
        lang = 'fa'
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
    return render(request, 'signup.html',
                  {'form': form, 'company': company_obj, 'api_methods': api_methods, 'lang': lang})


def login(request):
    lang = translation.get_language()
    if lang not in [p[0] for p in language_choices]:
        lang = 'fa'
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
    return render(request, 'login.html',
                  {'form': form, 'company': company_obj, 'api_methods': api_methods, 'lang': lang})


def logout_view(request):
    auth_logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    lang = translation.get_language()
    if lang not in [p[0] for p in language_choices]:
        lang = 'fa'
    company_obj = Company.objects.get(language=lang)
    api_methods = ApiMethod.objects.filter(language=lang)
    userAPI = UserAPI.objects.get(user=request.user)
    return render(request, 'profile.html',
                  {'userAPI': userAPI, 'company': company_obj, 'api_methods': api_methods, 'lang': lang})


def get_api_param(request):
    if request.method == 'POST':
        try:
            api_id = request.POST.get('api_id')
            if not api_id:
                return JsonResponse({'error': 'API ID is required.'}, status=400)
            api_method = get_object_or_404(ApiMethod, pk=api_id)
            api_params = ApiParam.objects.filter(api_method=api_method, language=api_method.language)
            param_list = [
                {
                    'id': param.id,
                    'name': param.name,
                    'description': param.description,
                    'type': param.type,
                }
                for param in api_params
            ]
            return JsonResponse({'api_params': param_list})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


def check_tokens(user):
    userAPI = UserAPI.objects.get(user=user)
    if userAPI.tokens <= 0:
        return False

    userAPI.tokens -= 1
    userAPI.save()
    return True


@csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def post_ocr(request):
    user = request.user
    if not check_tokens(user):
        return JsonResponse({'error': 'Insufficient tokens.'}, status=403)

    # Send the request to Flask
    response = requests.post(flask_url + "/ocr", files=request.FILES, data=request.POST)

    # Return the result to the user
    return JsonResponse(response.json())


@csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def post_classify(request):
    user = request.user
    if not check_tokens(user):
        return JsonResponse({'error': 'Insufficient tokens.'}, status=403)

    # Send the request to Flask
    response = requests.post(flask_url + "/classify", files=request.FILES, data=request.POST)

    # Return the result to the user
    return JsonResponse(response.json())


def method(request, pk):
    lang = translation.get_language()
    if lang not in [p[0] for p in language_choices]:
        lang = 'fa'
    api_method = get_object_or_404(ApiMethod, pk=pk)
    company_obj = Company.objects.get(language=lang)
    api_methods = ApiMethod.objects.filter(language=lang)
    # key = UserAPI.objects.get(user=request.user).key

    return render(request, 'document.html',
                  {'company': company_obj, 'api_method': api_method, 'api_methods': api_methods,
                   'lang': lang})


def api_method_list(request):
    lang = translation.get_language()
    if lang not in [p[0] for p in language_choices]:
        lang = 'fa'
    company_obj = Company.objects.get(language=lang)
    api_methods = ApiMethod.objects.filter(language=lang)
    return render(request, 'api_list.html', {'company': company_obj, 'api_methods': api_methods, 'lang': lang})


def active_language(request, lang):
    # Activate the requested language for the current request
    translation.activate(lang)

    # Create a response to redirect to the previous page
    response = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    # Set the language cookie (this will persist the language choice)
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang)

    return response


@login_required()
def demo_page(request):
    user = request.user
    lang = translation.get_language()
    if lang not in [p[0] for p in language_choices]:
        lang = 'fa'
    api_methods = ApiMethod.objects.filter(language=lang)
    key = UserAPI.objects.get(user=user).key
    return render(request, 'demo.html', {'api_methods': api_methods, 'key': key})
