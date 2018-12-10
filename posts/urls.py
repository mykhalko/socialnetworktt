from django.conf.urls import url

from .views import PostAPIView, PostListAPIView


app_name = 'posts'


urlpatterns = [
    url('^/(?P<id>[0-9]+)$', PostAPIView.as_view(), name='detail'),
    url('^/', PostListAPIView.as_view(), name='list')
]
