from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, LoginForm
from .models import ImageHistory
from .image_generator import generate_image
from django.core.files.base import ContentFile
from io import BytesIO
from django.http import HttpResponse
import os

def sign_up_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main_page')
    else:
        form = SignUpForm()
    return render(request, 'main/sign_up.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main_page')
    else:
        form = LoginForm()
    return render(request, 'main/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def main_page(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        if prompt:
            try:
                # Generate the image and get both the image object and the file path
                image, image_path = generate_image(prompt)

                # Save image to a BytesIO buffer to save to ImageHistory
                image_io = BytesIO()
                image.save(image_io, format='PNG')
                image_file = ContentFile(image_io.getvalue(), os.path.basename(image_path))

                # Save image history with the actual image file
                ImageHistory.objects.create(user=request.user, image=image_file)

                # Redirect to avoid resubmission on refresh
                return redirect('main_page')

            except Exception as e:
                # Handle any errors that occur during image generation
                return HttpResponse(f"Error: {str(e)}", status=500)

    user_history = ImageHistory.objects.filter(user=request.user)
    return render(request, 'main/main.html', {'history': user_history})

@login_required
def clear_history(request):
    user_history = ImageHistory.objects.filter(user=request.user)
    user_history.delete()  # Deletes the user's history
    return redirect('main_page')  # Redirect back to main page
