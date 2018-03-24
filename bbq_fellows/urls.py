from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import login, logout
from bbqcore.views import signup


urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout/', logout, {'next_page': '/'}, name='logout'),
    path('login/', login, {'template_name': 'bbqcore/login.html'}, name='login'),
    path('signup/', signup, name='signup'),
    path('', include('bbqplanner.urls')),
]
