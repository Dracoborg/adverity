# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from .forms import FiltersForm


# Create your views here.
class IndexView(FormView):

    template_name = "dashboard/index.html"
    form_class = FiltersForm

    def form_valid(self, form):
        print("form is valid")
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        initial.update(dict(self.request.GET))

        return initial

    def get_context_data(self, **kwargs):
        print(self.request.GET)
        print(dir(self))
        context = super().get_context_data()
        context.update(dict(self.request.GET))
        print(context)
        return context
