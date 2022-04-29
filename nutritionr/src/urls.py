from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('results/recipe', views.RecipeResultsView.as_view(), name='results-recipe'),
    path('results/food', views.FoodResultsView.as_view(), name='results-food')
]
