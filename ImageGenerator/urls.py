# ImageGenerator/urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.urls import path, include

# Redirect to login page if unauthenticated user lands on the home page
def landing_redirect(request):
    return redirect('login')

urlpatterns = [
    path('', landing_redirect),  # Redirect the root URL to the login page
    path('main/', include('main.urls')),  # Include your main app URLs
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
