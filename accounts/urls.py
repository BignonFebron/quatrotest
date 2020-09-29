from django.conf.urls import url
from . import views
from rest_framework.authtoken import views as tokenview

urlpatterns = [
    url(r'register/', views.register),
    url(r'login/',tokenview.obtain_auth_token),
    url(r'api_keys/',views.getkeys),
    url(r'restaurants/',views.getNearbyRestautants),

]