from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.institution_search, name='institution_search'),
    path('ajax/load-districts/', views.load_districts, name='ajax_load_districts'),
     path('institution/<int:pk>/', views.institution_detail, name='institution_detail'),
     path('institution/<int:institution_id>/complaint/', views.complaint_create, name='complaint_create'),
]
