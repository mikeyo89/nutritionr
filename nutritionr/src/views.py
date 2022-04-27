from django.shortcuts import render
from django.urls import reverse
from django.views import generic

# Create your views here.
class HomeView(generic.TemplateView):
    """ Landing/Index View of the Site. """
    template_name = 'home.html'

    def get_success_url(self):
        return reverse("search-view")