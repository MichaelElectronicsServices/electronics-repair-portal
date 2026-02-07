from django.urls import path
from . import views

urlpatterns = [
        path('', views.base, name='base'),
        path('tickets/', views.ticket_list, name='ticket_list'),
        path('tickets/create/', views.ticket_create, name='ticket_create'),
        path('tickets/<int:pk>/', views.ticket_detail, name='ticket_detail'),
        path('tickets/<int:pk>/update/', views.ticket_update, name='ticket_update'),
        path('tickets/<int:pk>/estimate/', views.estimate_create, name='estimate_create'),
        path('tickets/<int:pk>/schedule/', views.schedule_create, name='schedule_create'),

]

