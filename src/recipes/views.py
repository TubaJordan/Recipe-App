from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Recipe

# Create your views here.
def home(request):
    return render(request, "recipes/recipes_home.html")

class RecipeListView(ListView):
    model = Recipe
    template_name = "recipes/recipe_list.html"

class RecipeDetailView(DetailView):
    model = Recipe
    template_name = "recipes/recipe_details.html"