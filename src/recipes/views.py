from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Recipe
from .forms import SearchForm, RecipeForm
from .utils import get_popular_ingredients_chart, get_recipe_distribution_by_difficulty_chart, get_cooking_time_by_difficulty_chart
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from json.decoder import JSONDecodeError

import pandas as pd
import json


# View for the homepage
def home(request):
    # Render the home template
    return render(request, "recipes/recipes_home.html")

# View to add a new recipe
@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the valid form and return a success status
            form.save()
            return JsonResponse({'status': 'success'})
        else:
            # Return form errors as JSON if form is not valid
            return JsonResponse({'status': 'error', 'errors': form.errors})
    # Handle non-POST methods
    return JsonResponse({'status': 'invalid_method'})

# View to update an existing recipe
@login_required
def update_recipe(request, pk):
    # Retrieve the recipe or return a 404 if not found
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        print(form)
        if form.is_valid():
            # Save the updated form and redirect to the recipe detail page
            form.save()
            return redirect('recipes:detail', pk=recipe.pk)
    else:
        # If not a POST request, instantiate the form with the existing recipe
        form = RecipeForm(instance=recipe)
    # Render the template with the form and recipe instance
    return render(request, 'recipes/recipe_details.html', {'form': form, 'object': recipe})

@login_required
@require_POST
def delete_recipe(request, pk):
    try:
        # Attempt to parse the request body as JSON
        data = json.loads(request.body)
        confirmation_text = data.get('confirmation_text', '')
        
        # Check if the confirmation text matches the expected value
        if confirmation_text == "DELETE RECIPE":
             # Look up the Recipe object with the provided primary key (pk) and delete it
            recipe = get_object_or_404(Recipe, pk=pk)
            recipe.delete()
            # Respond with a success status in JSON format
            return JsonResponse({'status': 'success'})
        else:
            # Respond with an error status and message if the confirmation text does not match
            return JsonResponse({'status': 'error', 'message': 'Incorrect confirmation text'})
    except JSONDecodeError:
        # Handle cases where the request body does not contain valid JSON
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)


# Class-based view to list recipes, requiring user login. Inherits from LoginRequiredMixin for authentication and ListView for object listing functionality.
class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe # Specifies the Recipe model to be used by the ListView.
    template_name = "recipes/recipe_list.html" # The template used to render the list of recipes.

    # Overrides the get_queryset method to customize the retrieval of the recipe list based on search parameters.
    def get_queryset(self):
        queryset = super().get_queryset() # Calls the parent class's get_queryset method to get the initial queryset.

        # Retrieve search parameters from the request's GET dictionary.
        search_term = self.request.GET.get("search_term")
        ingredient = self.request.GET.get("ingredient")
        difficulty = self.request.GET.get("difficulty")
        description = self.request.GET.get("description")

        # Filters the queryset based on the provided search parameters.
        if search_term:
            queryset = queryset.filter(name__icontains=search_term)
        if ingredient:
            queryset = queryset.filter(ingredients__icontains=ingredient)
        if difficulty and difficulty != '':
            queryset = queryset.filter(difficulty=difficulty)
        if description:
            queryset = queryset.filter(description__icontains=description)

        # Filters for cooking time using both minimum and maximum values.
        min_cooking_time = self.request.GET.get("min_cooking_time")
        max_cooking_time = self.request.GET.get("max_cooking_time")
        if min_cooking_time and max_cooking_time:
            queryset = queryset.filter(cooking_time__gte=min_cooking_time, cooking_time__lte=max_cooking_time)
        elif min_cooking_time:
            queryset = queryset.filter(cooking_time__gte=min_cooking_time)
        elif max_cooking_time:
            queryset = queryset.filter(cooking_time__lte=max_cooking_time)

        return queryset # Returns the filtered queryset.
    
    # Overrides the get_context_data method to add additional context to the template.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # Calls the parent class's get_context_data method to get the initial context.
        queryset = self.get_queryset()  # Fetches the current queryset after applying filters.
        
        # Converts the queryset to a DataFrame, then to a list of dictionaries to add URLs for each recipe instance.
        df = pd.DataFrame(list(queryset.values('id', 'name', 'description', 'pic', 'cooking_time')))
        recipes = df.to_dict("records") if not df.empty else []
        for recipe in recipes:
            recipe_instance = Recipe.objects.get(pk=recipe["id"])
            recipe["get_absolute_url"] = recipe_instance.get_absolute_url()
            recipe["pic_url"] = recipe_instance.pic.url if recipe_instance.pic else None
        
        context["object_list"] = recipes # Adds the modified list of recipes to the context.
        
        # Adds the modified list of recipes to the context.
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

        # Additional context for search form and charts based on the filtered recipes.  
        recipes_list = list(queryset.values('id', 'name', 'ingredients', 'description', 'pic', 'cooking_time', 'difficulty'))
        context["search_form"] = SearchForm(self.request.GET)  # Retain the search form input
        context['show_all_recipes_button'] = bool(self.request.GET)
        # Adds charts for popular ingredients, recipe difficulty distribution, and cooking time by difficulty to the context.
        context["popular_ingredients_chart"] = get_popular_ingredients_chart(recipes_list)
        context["recipe_difficulty_distribution_chart"] = get_recipe_distribution_by_difficulty_chart(recipes_list)
        context["cooking_time_by_difficulty_chart"] = get_cooking_time_by_difficulty_chart(recipes_list)

        return context # Returns the enriched context.


# A view for showing details of a single Recipe, accessible only to logged-in users.
class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe # Specifies the Recipe model this view will detail.
    template_name = "recipes/recipe_details.html" # The template to use for displaying the recipe's details.

    # Adds extra information to the context passed to the template.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # Adds extra information to the context passed to the template.
        
        recipe = self.get_object() # Retrieves the specific Recipe object being viewed.
        context['form'] = RecipeForm(instance=recipe)  # Adds a form populated with the recipe's data to the context.
        return context

        context.update({
            'search_params': self.request.GET.urlencode()
        })
        return context
    