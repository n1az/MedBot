
from django.contrib import admin
from django.urls import path, include
from medbot_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('medbot_app.urls')),
]
