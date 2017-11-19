from django.conf import settings
from django.conf.urls import url, include
from django.views.decorators.csrf import csrf_exempt

from graphene_django.views import GraphQLView as Dupa
from graphene_extensions.views import GraphQLView

from .schema import schema


urlpatterns = [
    url(r'^graphql-django', Dupa.as_view(graphiql=True)),
    url(r'^graphql', csrf_exempt(GraphQLView.as_view(schema=schema))),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
