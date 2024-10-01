"""
URL configuration for lms_portal project.

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
from .views import *
urlpatterns = [
    path('', home, name='home'),  # Redirect root URL to the home view
    path('admin/', admin.site.urls),
    path('home/', home, name='home'), 
    path('readers/', readers, name='readers'),
    path('books/', books, name='books'),
    path('mybag/', mybag, name='mybag'),
    path('returns/', returns, name='returns'),  
    path('readers/add/', save_reader, name='save_reader'),  
    path('books/add/', save_book, name='add_book'),  
    path('search_books/', search_books, name='search_books'),  
    path('books/add_to_bag/<int:book_id>/', add_to_bag, name='add_to_bag'),  
    path('mybag/remove_from_bag/<int:book_id>/', remove_from_bag, name='remove_from_bag'),  
    path('checkout/', checkout, name='checkout'),
    path('readers/reader_search/', reader_search, name='reader_search')
]
