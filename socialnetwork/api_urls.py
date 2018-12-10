from django.conf.urls import url, include


app_name = 'api'


urlpatterns = [
    url(r'^posts', include('posts.urls', namespace='posts')),
    url(r'^', include('accounts.urls', namespace='accounts'))
]
