from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('bbqcreate/', views.CreateEvent.as_view(), name='event_create'),
    path('bbqregistered/', views.EventRegistrationSuccess.as_view(), name='event_register_success'),
    path('bbqevents/<str:uuid>/', views.Event.as_view(), name='event'),
    path('bbqevents/', views.ListEvents.as_view(), name='events'),
    path('', views.index, name='index'),
]
