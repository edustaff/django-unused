from django.conf.urls import include, url
from example.server.views.view_not_named_view import UsedView

urlpatterns = [
    url(r'^$', UsedView.as_view(), name='used'),
]
