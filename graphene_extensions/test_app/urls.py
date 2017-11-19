from django.conf import settings
from django.conf.urls import url, include

from graphene_django.views import GraphQLView

urlpatterns = [
    url(r'^graphql', GraphQLView.as_view(graphiql=True)),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
