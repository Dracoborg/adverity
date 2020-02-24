# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from .forms import FiltersForm


# Create your views here.
class IndexView(FormView):

    template_name = "dashboard/index.html"
    form_class = FiltersForm


    def get_initial(self):
        """ initialize form with data from GET request """
        initial = super().get_initial()
        initial.update(dict(self.request.GET))

        return initial

    def get_context_data(self, **kwargs):
        """ return context for the view """

        context = super().get_context_data()
        context.update(dict(self.request.GET))
        return context
