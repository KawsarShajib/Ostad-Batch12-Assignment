from django.urls import path
from . import views

app_name = 'rentals'

urlpatterns = [
    path('request/<int:property_id>/', views.send_request, name='send_request'),
    path('my-requests/', views.my_requests, name='my_requests'),
    path('cancel/<int:pk>/', views.cancel_request, name='cancel_request'),
    path('owner/', views.owner_requests, name='owner_requests'),
    path('owner/accept/<int:pk>/', views.accept_request, name='accept_request'),
    path('owner/reject/<int:pk>/', views.reject_request, name='reject_request'),
    path('review/<int:property_id>/', views.add_review, name='add_review'),
]
