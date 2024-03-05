from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import SearchForm, RecipeForm
from .models import Recipe
import json


# Tests the validity and cooking time validation logic of the SearchForm.
class SearchFormTest(TestCase):

    def test_form_validity(self):
        # Tests if the form is valid both with all fields filled and with only the mandatory fields filled.
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
        # Checks the form's handling of invalid cooking time values, ensuring validation works as expected.
        form_data_invalid = {
            'min_cooking_time': -5,
            'max_cooking_time': 'not a number'
        }
        form_invalid = SearchForm(data=form_data_invalid)
        self.assertFalse(form_invalid.is_valid())

# Verifies the creation and field attributes of the Recipe model.
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
        # Confirms a Recipe instance is correctly created and its string representation matches its name.
        self.assertTrue(isinstance(self.recipe, Recipe))
        self.assertEqual(self.recipe.__str__(), self.recipe.name)
    
    def test_name_max_length(self):
        # Ensures the name field's maximum length attribute is correctly defined.
        max_length = self.recipe._meta.get_field('name').max_length
        self.assertEqual(max_length, 50)
    
    def test_recipe_name(self):
        # Checks the verbose name of the name field.
        recipe_name_label = self.recipe._meta.get_field('name').verbose_name
        self.assertEqual(recipe_name_label, 'name')
    
    def test_difficulty_max_length(self):
        # Verifies the difficulty field's maximum length is correctly set.
        max_length = self.recipe._meta.get_field('difficulty').max_length
        self.assertEqual(max_length, 20)

    def test_string_representation(self):
        # Tests the string representation of a Recipe object to ensure it returns its name.
        self.assertEqual(str(self.recipe), self.recipe.name)
    
    def test_return_ingredients_as_list(self):
        # Confirms ingredients stored as a string are correctly converted to a list.
        ingredients_list = self.recipe.return_ingredients_as_list()
        self.assertEqual(len(ingredients_list), 3)
    
    def test_calculate_difficulty(self):
        # Tests the logic that calculates a recipe's difficulty based on cooking time and ingredient count.
        self.recipe.cooking_time = 5
        self.recipe.ingredients = 'Ingredient1,Ingredient2'
        self.recipe.save()
        self.assertEqual(self.recipe.difficulty, 'Easy')
    
        self.recipe.cooking_time = 15
        self.recipe.ingredients = 'Ingredient1,Ingredient2,Ingredient3,Ingredient4'
        self.recipe.save()
        self.assertEqual(self.recipe.difficulty, 'Hard')
        
    def test_save_method_override(self):
        # Checks if the save method correctly sets the difficulty level based on cooking time and ingredients.
        self.recipe.cooking_time = 20
        self.recipe.ingredients = 'Ingredient1,Ingredient2,Ingredient3'
        self.recipe.save()
        self.assertEqual(self.recipe.difficulty, 'Intermediate')
    
    def test_default_image_path(self):
        # Verifies that the default path for a recipe's image is correctly set.
        self.assertEqual(self.recipe.pic, 'no_picture')

# Tests custom methods of the Recipe model related to URL retrieval and ingredient list formatting.
class RecipeModelMethodTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345')
        cls.recipe = Recipe.objects.create(
            name='Test Recipe Method',
            ingredients='Ingredient1,Ingredient2,Ingredient3',
            cooking_time=30,
            difficulty='Easy',
            description='Test method description'
        )
    
    def test_get_absolute_url(self):
        # Ensures the method correctly returns the absolute URL for a recipe detail view.
        expected_url = reverse('recipes:detail', kwargs={'pk': self.recipe.pk})
        self.assertEqual(self.recipe.get_absolute_url(), expected_url)
    
    def test_return_ingredients_as_list(self):
        # Same as in RecipeModelTest, it verifies the correct conversion of ingredients to a list.
        ingredients_list = self.recipe.return_ingredients_as_list()
        self.assertEqual(len(ingredients_list), 3)

# Ensures the correct functionality and access control of views related to recipes.
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

    def test_login_required_for_list_view(self):
        # Checks if accessing the list view without authentication correctly redirects to the login page.
        response = self.client.get('/list/')
        self.assertRedirects(response, '/login/?next=/list/')

    def test_login_required_for_detail_view(self):
        # Similar to the list view test, it ensures the detail view requires user authentication.
        response = self.client.get(f'/list/{self.recipe.pk}/')
        self.assertRedirects(response, f'/login/?next=/list/{self.recipe.pk}/')
    
    def test_home_page_status_code(self):
        # Verifies that the home page is accessible and returns the correct HTTP status code.
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_recipe_list_view(self):
    # Tests accessibility of the recipe list view when logged in.
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('recipes:list'))
        self.assertEqual(response.status_code, 200)
    
    def test_recipe_detail_view(self):
    # Confirms that the recipe detail view is accessible for an existing recipe when logged in.
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('recipes:detail', args=[self.recipe.pk]))
        self.assertEqual(response.status_code, 200)
    
    def test_recipe_detail_view_with_nonexistent_recipe(self):
    # Checks how the detail view handles a non-existent recipe (expects a 404 status).
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('recipes:detail', args=[999]))
        self.assertEqual(response.status_code, 404)

# Tests AJAX views for adding, updating, and deleting recipes.
class RecipeAjaxViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345')
        cls.recipe = Recipe.objects.create(
            name='Ajax Test Recipe',
            ingredients='Ingredient1,Ingredient2',
            cooking_time=15,
            difficulty='Easy',
            description='Ajax Test Description',
            pic='test_pic.jpg'
        )
    
    def setUp(self):
        self.client = Client()
        self.client.login(username='testuser', password='12345')

    def test_add_recipe_ajax(self):
        # Verifies that a recipe can be added successfully via AJAX and returns the correct response.
        url = reverse('recipes:add_recipe')
        data = {
            'name': 'New Ajax Recipe',
            'ingredients': 'Ingredient1,Ingredient2,Ingredient3',
            'cooking_time': 20,
            'description': 'New test recipe description',
        }
        response = self.client.post(url, data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['status'], 'success')

    def test_update_recipe_ajax(self):
        # Tests updating a recipe's details via AJAX and ensures the changes are persisted.
        url = reverse('recipes:update_recipe', args=[self.recipe.pk])
        updated_data = {
            'name': 'Updated Ajax Recipe',
            'ingredients': 'Ingredient1,Ingredient2,UpdatedIngredient3',
            'cooking_time': 25,
            'description': 'Updated test recipe description',
        }
        response = self.client.post(url, updated_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.recipe.refresh_from_db()
        self.assertEqual(self.recipe.name, 'Updated Ajax Recipe')
        self.assertEqual(response.status_code, 302)  # Confirm that a redirect occurs

    def test_delete_recipe_ajax(self):
        # Confirms that a recipe can be deleted via AJAX, and the response reflects the success of the operation.
        url = reverse('recipes:delete_recipe', args=[self.recipe.pk])
        data = json.dumps({'confirmation_text': 'DELETE RECIPE'})
        response = self.client.post(url, data, content_type='application/json', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['status'], 'success')
        with self.assertRaises(Recipe.DoesNotExist):
            Recipe.objects.get(pk=self.recipe.pk)

# Specific test cases for RecipeForm validations.
class RecipeFormTestExtended(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='extended_user', password='password')
    
    def test_recipe_form_with_empty_ingredients(self):
        # Checks form validity when the ingredients field is empty, expecting it to fail.
        form_data = {
            'name': 'Test Recipe With No Ingredients',
            'ingredients': '',
            'cooking_time': 10,
            'description': 'Recipe without ingredients'
        }
        form = RecipeForm(data=form_data)
        self.assertFalse(form.is_valid())

# Tests for the validity of RecipeForm under various conditions.
class RecipeFormTest(TestCase):

    def test_recipe_form_valid(self):
        # Verifies that the form is valid with all fields correctly filled out.
        form_data = {
            'name': 'Chocolate Cake',
            'ingredients': 'Chocolate, Flour, Sugar, Eggs',
            'cooking_time': 45,
            'description': 'Delicious chocolate cake recipe',
        }
        form = RecipeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_recipe_form_invalid_no_name(self):
        # Tests form validity when the name field is empty, expecting an error.
        form_data = {
            'name': '',
            'ingredients': 'Chocolate, Flour, Sugar, Eggs',
            'cooking_time': 45,
            'description': 'Delicious chocolate cake recipe',
        }
        form = RecipeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_recipe_form_invalid_negative_cooking_time(self):
        # Ensures the form is considered invalid with a negative cooking time.
        form_data = {
            'name': 'Chocolate Cake',
            'ingredients': 'Chocolate, Flour, Sugar, Eggs',
            'cooking_time': -20,
            'description': 'Delicious chocolate cake recipe',
        }
        form = RecipeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('cooking_time', form.errors)

    def test_recipe_form_minimal_valid_data(self):
        # Confirms that the form is valid with just the minimal required data.
        form_data = {
            'name': 'Simple Bread',
            'ingredients': 'Flour, Water, Yeast',
            'cooking_time': 30,
            'description': 'A very simple bread recipe.',
        }
        form = RecipeForm(data=form_data)
        self.assertTrue(form.is_valid())

# Ensures proper permission handling for recipe-related actions.
class RecipePermissionTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user', password='password')
        self.recipe = Recipe.objects.create(
            name='Test Recipe',
            ingredients='Test Ingredients',
            cooking_time=10,
            description='Test Description'
        )
        self.login_url = reverse('login')

    def test_create_recipe_authenticated(self):
        # Tests that an authenticated user can create a recipe.
        self.client.login(username='user', password='password')
        response = self.client.post(reverse('recipes:add_recipe'), {
            'name': 'New Recipe',
            'ingredients': 'Some Ingredients',
            'cooking_time': 20,
            'description': 'Some Description'
        })
        self.assertIn(response.status_code, [200, 302])

    def test_create_recipe_unauthenticated(self):
        # Checks that an unauthenticated user is redirected to the login page when attempting to create a recipe.
        response = self.client.get(reverse('recipes:add_recipe'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.login_url in response['Location'])

    def test_update_recipe_authenticated(self):
        # Verifies that an authenticated user can update a recipe.
        self.client.login(username='user', password='password')
        response = self.client.post(reverse('recipes:update_recipe', args=[self.recipe.id]), {
            'name': 'Updated Recipe Name',
            'ingredients': 'Updated Ingredients',
            'cooking_time': 15,
            'description': 'Updated Description'
        })
        self.assertIn(response.status_code, [200, 302])

    def test_delete_recipe_authenticated(self):
        # Confirms that an authenticated user can delete a recipe, and the operation reflects success in the response.
        self.client.login(username='user', password='password')
        data = json.dumps({'confirmation_text': 'DELETE RECIPE'})
        response = self.client.post(reverse('recipes:delete_recipe', args=[self.recipe.id]), data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['status'], 'success')