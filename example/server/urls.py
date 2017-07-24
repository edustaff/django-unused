from django.conf.urls import include, url
from django.contrib import admin

from example.server.views.view_not_named_view import ServerView

urlpatterns = [
    # Examples:
    # url(r'^$', 'example.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^server/', ServerView.as_view(), name='server'),
    url(r'^used/', include('example.app1.urls', namespace='used')),
]
