from django import forms

class SearchForm(forms.Form):
    search_term = forms.CharField(required=False, label="Search by name")
    ingredient = forms.CharField(required=False, label="Search by ingredient")
    difficulty = forms.ChoiceField(choices=[('', 'Any Difficulty'), ('Easy', 'Easy'), ('Medium', 'Medium'), ('Intermediate', 'Intermediate'), ('Hard', 'Hard')], required=False, label="Search by difficulty")
    min_cooking_time = forms.IntegerField(required=False, label="Minimum cooking time (minutes)", min_value=0)
    max_cooking_time = forms.IntegerField(required=False, label="Maximum cooking time (minutes)", min_value=0) 
    description = forms.CharField(required=False, label="Search by description")