from django import forms
from django.forms import ModelForm, TextInput, Textarea, NumberInput, FileInput
from .models import Recipe

class SearchForm(forms.Form):
    # Define form fields for searching recipes.
    search_term = forms.CharField(required=False, label="Search by name") # Optional search term by recipe name.
    ingredient = forms.CharField(required=False, label="Search by ingredient") # Optional search by ingredient.
    # Choice field for filtering by difficulty, with an option to select any difficulty.
    difficulty = forms.ChoiceField(choices=[('', 'Any Difficulty'), ('Easy', 'Easy'), ('Medium', 'Medium'), ('Intermediate', 'Intermediate'), ('Hard', 'Hard')], required=False, label="Search by difficulty")
    min_cooking_time = forms.IntegerField(required=False, label="Minimum cooking time (minutes)", min_value=0) # Optional minimum cooking time filter.
    max_cooking_time = forms.IntegerField(required=False, label="Maximum cooking time (minutes)", min_value=0) # Optional maximum cooking time filter.
    description = forms.CharField(required=False, label="Search by description") # Optional search by description.

class RecipeForm(ModelForm):
    # Custom field definition for the recipe image, making it optional and applying custom styling.
    pic = forms.ImageField(label='Picture', required=False, widget=forms.FileInput(attrs={'class': 'form-control picture-change'}))
    
    class Meta:
        model = Recipe # Specify the model to be used to generate this form.
        fields = ['name', 'ingredients', 'cooking_time', 'description', 'pic'] # Specify the model fields to include in the form.
        # Define custom widgets for form fields, applying Bootstrap 'form-control' class for styling.
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'ingredients': TextInput(attrs={'class': 'form-control'}),
            'cooking_time': NumberInput(attrs={'class': 'form-control'}),
            'description': TextInput(attrs={'class': 'form-control'}),
        }