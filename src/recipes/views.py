from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Recipe
from .forms import SearchForm
from .utils import get_popular_ingredients_chart, get_recipe_distribution_by_difficulty_chart, get_cooking_time_by_difficulty_chart

import pandas as pd

# Create your views here.
def home(request):
    return render(request, "recipes/recipes_home.html")

class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = "recipes/recipe_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.GET.get("search_term")
        ingredient = self.request.GET.get("ingredient")
        difficulty = self.request.GET.get("difficulty")
        description = self.request.GET.get("description")

        if search_term:
            queryset = queryset.filter(name__icontains=search_term)
        if ingredient:
            queryset = queryset.filter(ingredients__icontains=ingredient)
        if difficulty and difficulty != '':
            queryset = queryset.filter(difficulty=difficulty)
        if description:
            queryset = queryset.filter(description__icontains=description)

        min_cooking_time = self.request.GET.get("min_cooking_time")
        max_cooking_time = self.request.GET.get("max_cooking_time")

        if min_cooking_time and max_cooking_time:
            queryset = queryset.filter(cooking_time__gte=min_cooking_time, cooking_time__lte=max_cooking_time)
        elif min_cooking_time:
            queryset = queryset.filter(cooking_time__gte=min_cooking_time)
        elif max_cooking_time:
            queryset = queryset.filter(cooking_time__lte=max_cooking_time)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()  # Fetch the current queryset
        
        df = pd.DataFrame(list(queryset.values('id', 'name', 'description', 'pic', 'cooking_time')))

        recipes = df.to_dict("records") if not df.empty else []

        for recipe in recipes:
            recipe_instance = Recipe.objects.get(pk=recipe["id"])
            recipe["get_absolute_url"] = recipe_instance.get_absolute_url()
            recipe["pic_url"] = recipe_instance.pic.url if recipe_instance.pic else None
        
        context["object_list"] = recipes
        
        num_results = len(context["object_list"])
        title_parts = []

        search_term = self.request.GET.get("search_term")
        ingredient = self.request.GET.get("ingredient")
        difficulty = self.request.GET.get("difficulty")
        min_cooking_time = self.request.GET.get("min_cooking_time")
        max_cooking_time = self.request.GET.get("max_cooking_time")
        description = self.request.GET.get("description")

        if search_term:
            title_parts.append(f"'{search_term}' in the name")
        if ingredient:
            title_parts.append(f"'{ingredient}' in ingredients")
        if difficulty and difficulty != '':
            title_parts.append(f"difficulty of {difficulty}")
        if min_cooking_time and max_cooking_time:
            title_parts.append(f"cooking time: {min_cooking_time} to {max_cooking_time} minutes")
        elif min_cooking_time:
            title_parts.append(f"cooking time: {min_cooking_time} minutes and higher")
        elif max_cooking_time:
            title_parts.append(f"cooking time: below {max_cooking_time} minutes")
        if description:
            title_parts.append(f"'{description}' in description")

        # Constructing the main title and detailed search criteria
        if title_parts:
            context['main_title'] = "Your search results for:"
            recipe_word = "Recipe" if num_results == 1 else "Recipes"
            details_intro = f"{recipe_word} with "  # Adjust the intro based on number of results
            context['search_details'] = details_intro + ", ".join(title_parts)
        else:
            context['main_title'] = "Full List of Recipes"
            context['search_details'] = ""

        recipes_list = list(queryset.values('id', 'name', 'ingredients', 'description', 'pic', 'cooking_time', 'difficulty'))

        context["search_form"] = SearchForm(self.request.GET)  # Retain the search form input
        context['show_all_recipes_button'] = bool(self.request.GET)
        context["popular_ingredients_chart"] = get_popular_ingredients_chart(recipes_list)
        context["recipe_difficulty_distribution_chart"] = get_recipe_distribution_by_difficulty_chart(recipes_list)
        context["cooking_time_by_difficulty_chart"] = get_cooking_time_by_difficulty_chart(recipes_list)

        return context

class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = "recipes/recipe_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the current query parameters to the template.
        context.update({
            'search_params': self.request.GET.urlencode()
        })
        return context
    

