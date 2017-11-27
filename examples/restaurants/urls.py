from django.conf.urls import url

from graphene_extensions.views import GraphQLView

from .schema import schema

urlpatterns = [
    url(r'graphql', GraphQLView.as_view(schema=schema))
]
