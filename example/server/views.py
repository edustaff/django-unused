from django.views.generic import TemplateView


class ServerView(TemplateView):
    template_name = 'server/used_in_view.html'
