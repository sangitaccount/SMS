from django.conf.urls import include, url
from . import views

urlpatterns = [
        url(r'^$',views.login_user,name='login'),
        url(r'request$',views.process_request,name='request'),
]
