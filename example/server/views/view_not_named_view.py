from django.views.generic import TemplateView


class UsedView(TemplateView):
    template_name = 'server/used_in_view.html'


class UnusedView(TemplateView):
    template_name = ''


class ServerView(UsedView):
    template_name = 'server/used_in_view.html'
