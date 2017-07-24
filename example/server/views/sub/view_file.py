from app1.views import *
from django_unused.unused.decorators import used_view


@used_view
class SubApp1View(App1View):
    template_name = 'app1/used_in_view.html'