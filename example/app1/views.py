from django.views.generic import TemplateView


class App1View(TemplateView):
    template_name = 'app1/used_in_view.html'
