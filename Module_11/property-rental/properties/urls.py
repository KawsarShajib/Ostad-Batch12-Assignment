from django.urls import path
from . import views

app_name = 'properties'

urlpatterns = [
    path('', views.property_list, name='list'),
    path('properties/mine/', views.my_properties, name='mine'),
    path('properties/create/', views.property_create, name='create'),
    path('properties/<int:pk>/', views.property_detail, name='detail'),
    path('properties/edit/<int:pk>/', views.property_update, name='update'),
    path('properties/delete/<int:pk>/', views.property_delete, name='delete'),
    # addition of image gallery for a property
    path('properties/image/delete/<int:pk>/', views.delete_property_image, name='delete_image'),
]
