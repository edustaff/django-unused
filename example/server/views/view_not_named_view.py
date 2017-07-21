from django.views.generic import ListView


class UnusedView(ListView):

    def get_context_data(self, **kwargs):
        context = super(UnusedView, self).get_context_data(**kwargs)
        return context