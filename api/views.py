import numpy as np
from PIL import Image
from io import BytesIO
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib import messages

from .forms import *
from .models import language_choices
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

    company_obj = Company.objects.get(language=lang)
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form, 'company': company_obj})


def login(request):
    lang = request.GET.get('lang', 'en')
    if lang not in [p[0] for p in language_choices]:
        lang = 'en'

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
    return render(request, 'login.html', {'form': form, 'company': company_obj})


def logout_view(request):
    auth_logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    userAPI = UserAPI.objects.get(user=request.user)
    return render(request, 'profile.html', {'userAPI': userAPI})


def convert_image_to_numpy_array(image_file):
    image = Image.open(image_file)

    image_array = np.array(image)

    return image_array

@csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def endpoint(request):
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

    if method == "OCRPicture":
        pass

    userAPI = UserAPI.objects.get(user=user)
    if userAPI.tokens <= 0:
        return JsonResponse({'error': 'Insufficient tokens.'}, status=403)

    userAPI.tokens -= 1
    userAPI.save()
    # Process the image and method here
    # Example: save the image, perform an action based on the method, etc.

    # Example response after processing
    return JsonResponse({'success': 'Image processed successfully.', 'image size': image_array.shape, 'method': method},
                        status=200)
