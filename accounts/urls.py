from django.conf.urls import url
from .views import SignupAPIView
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token


app_name = 'accounts'


urlpatterns = [
    url(r'^signup', SignupAPIView.as_view(), name='signup'),
    url(r'^token-auth', obtain_jwt_token, name='auth'),
    url(r'^token-refresh', refresh_jwt_token, name='refresh')
]
