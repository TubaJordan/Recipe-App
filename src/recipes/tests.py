from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .forms import SearchForm
from .models import Recipe


class SearchFormTest(TestCase):

    def test_form_validity(self):
        # Form with all fields filled
        form_data = {
            'search_term': 'cake',
            'ingredient': 'flour',
            'difficulty': 'Easy',
            'min_cooking_time': 10,
            'max_cooking_time': 30,
            'description': 'delicious'
        }
        form = SearchForm(data=form_data)
        self.assertTrue(form.is_valid())

        # Form with only some fields filled
        form_data_partial = {
            'search_term': 'cake',
            'difficulty': 'Easy'
        }
        form_partial = SearchForm(data=form_data_partial)
        self.assertTrue(form_partial.is_valid())

    def test_cooking_time_validation(self):
        # Test with invalid cooking time
        form_data_invalid = {
            'min_cooking_time': -5,  # Invalid value
            'max_cooking_time': 'not a number'  # Invalid value
        }
        form_invalid = SearchForm(data=form_data_invalid)
        self.assertFalse(form_invalid.is_valid())




class RecipeModelTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        # Set up a Recipe object once for all test methods in this class.
        cls.recipe = Recipe.objects.create(
            name='Test Recipe',
            ingredients='Ingredient1,Ingredient2,Ingredient3',
            cooking_time=30,
            difficulty='Easy',
            description='Test Description'
        )
    
    def test_recipe_creation(self):
        # Test that a Recipe object is correctly created.
        self.assertTrue(isinstance(self.recipe, Recipe))
        self.assertEqual(self.recipe.__str__(), self.recipe.name)
    
    def test_name_max_length(self):
        # Ensure the 'name' field max_length attribute is correctly set.
        max_length = self.recipe._meta.get_field('name').max_length
        self.assertEqual(max_length, 50)
    
    def test_recipe_name(self):
        # Check that the 'name' field's verbose name is as expected.
        recipe_name_label = self.recipe._meta.get_field('name').verbose_name
        self.assertEqual(recipe_name_label, 'name')
    
    def test_difficulty_max_length(self):
        # Verify the 'difficulty' field's max_length is set as expected.
        max_length = self.recipe._meta.get_field('difficulty').max_length
        self.assertEqual(max_length, 20)

    def test_string_representation(self):
        # Test the string representation of a Recipe object (should be its name).
        self.assertEqual(str(self.recipe), self.recipe.name)
    
    def test_return_ingredients_as_list(self):
        # Ensure the ingredients are correctly split into a list.
        ingredients_list = self.recipe.return_ingredients_as_list()
        self.assertEqual(len(ingredients_list), 3)
    
    def test_calculate_difficulty(self):
        # Test the difficulty calculation for various scenarios.
        self.recipe.cooking_time = 5
        self.recipe.ingredients = 'Ingredient1,Ingredient2'
        self.recipe.save()
        self.assertEqual(self.recipe.difficulty, 'Easy')
        
        self.recipe.cooking_time = 15
        self.recipe.ingredients = 'Ingredient1,Ingredient2,Ingredient3,Ingredient4'
        self.recipe.save()
        self.assertEqual(self.recipe.difficulty, 'Hard')
        
    def test_save_method_override(self):
        # Check that the difficulty is correctly set when a Recipe is saved.
        self.recipe.cooking_time = 20
        self.recipe.ingredients = 'Ingredient1,Ingredient2,Ingredient3'
        self.recipe.save()
        self.assertEqual(self.recipe.difficulty, 'Intermediate')
    
    def test_default_image_path(self):
        # Verify the default image path is set as expected.
        self.assertEqual(self.recipe.pic, 'no_picture')




class RecipeViewsTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345')
        # Set up data for the view tests.
        cls.recipe = Recipe.objects.create(
            name='View Test Recipe',
            ingredients='Ingredient1,Ingredient2,Ingredient3',
            cooking_time=20,
            difficulty='Medium',
            description='View Test Description'
        )

    # For the test_login_required_for_list_view
    def test_login_required_for_list_view(self):
        response = self.client.get('/list/')
        self.assertRedirects(response, '/login/?next=/list/')

    # For the test_login_required_for_detail_view
    def test_login_required_for_detail_view(self):
        response = self.client.get(f'/list/{self.recipe.pk}/')
        self.assertRedirects(response, f'/login/?next=/list/{self.recipe.pk}/')
    
    def test_home_page_status_code(self):
        # Test the home page is accessible and returns a HTTP 200 status.
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_recipe_list_view(self):
    # Log in before making the request
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('recipes:list'))
        self.assertEqual(response.status_code, 200)
    
    def test_recipe_detail_view(self):
    # Log in before making the request
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('recipes:detail', args=[self.recipe.pk]))
        self.assertEqual(response.status_code, 200)
    
    def test_recipe_detail_view_with_nonexistent_recipe(self):
    # Log in before making the request
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('recipes:detail', args=[999]))
        self.assertEqual(response.status_code, 404)
