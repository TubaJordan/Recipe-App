from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import home, RecipeListView, RecipeDetailView, add_recipe, update_recipe, delete_recipe

app_name = "recipes" # Define the application namespace for URL names.

urlpatterns = [
    path("", home), # Map the home view to the root URL of the app.
    path("list/", RecipeListView.as_view(), name="list"), # Map the RecipeListView to '/list/', named 'list'.
    path("list/<int:pk>/", RecipeDetailView.as_view(), name="detail"), # Map RecipeDetailView to '/list/<int:pk>/', where 'pk' is a placeholder for the recipe ID, named 'detail'.
    path("add/", add_recipe, name="add_recipe"), # Map the add_recipe view to '/add/', named 'add_recipe'.
    path('update/<int:pk>/', update_recipe, name='update_recipe'), # Map the update_recipe view to '/update/<int:pk>/', using 'pk' as a placeholder for the recipe ID, named 'update_recipe'.
    path('delete/<int:pk>/', csrf_exempt(delete_recipe), name='delete_recipe'), # Map the delete_recipe view to '/delete/<int:pk>/', exempt from CSRF checks, using 'pk' as a placeholder for the recipe ID, named 'delete_recipe'.
]