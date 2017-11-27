from django.conf.urls import url, include

urlpatterns = [
    url(r'restaurants', include('examples.restaurants.urls')),
]
