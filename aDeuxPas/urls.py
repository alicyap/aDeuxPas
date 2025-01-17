"""
URL configuration for aDeuxPas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

import ADP
from ADP import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.accueil, name='accueil'),  # Page d'accueil  # Page de la carte
    path('map/', views.map_view, name='map_view'), # Map.html
    path('line/<int:line_id>/', views.get_line_data, name='line_data'),
    path('get-lines/', views.get_lines, name='get_lines'),
    path('line/<str:line_id>/stations/', views.get_line_stations, name='line_stations'),
    # path('restaurants/', views.restaurants, name='restaurants'),
    # path('get-restaurant-data/', views.get_restaurant_data, name='get_restaurant_data')

]
