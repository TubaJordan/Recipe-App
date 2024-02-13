from django.test import TestCase
from .models import Recipe

class RecipeModelTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        # Set up a Recipe object once for all test methods in this class.
        Recipe.objects.create(
            name='Test Recipe',
            ingredients='Test Ingredients',
            cooking_time=30,
            difficulty='Easy',
            description='Test Description'
        )
    
    # Tests that a Recipe object is created and retrievable from the database.
    def test_recipe_creation(self):
        recipe = Recipe.objects.get(id=1)
        self.assertTrue(isinstance(recipe, Recipe))
        self.assertEqual(recipe.__str__(), recipe.name)
    
    # Ensures the 'name' field max_length is set to 50.
    def test_name_max_length(self):
        recipe = Recipe.objects.get(id=1)
        max_length = recipe._meta.get_field('name').max_length
        self.assertEqual(max_length, 50)

    # Checks the verbose name of the 'name' field is 'name'.
    def test_recipe_name(self):
        recipe = Recipe.objects.get(id=1)
        recipe_name_label = recipe._meta.get_field('name').verbose_name
        self.assertEqual(recipe_name_label, 'name')

    # Confirms the 'difficulty' field max_length is set to 20.
    def test_difficulty_max_length(self):
        recipe = Recipe.objects.get(id=1)
        max_length = recipe._meta.get_field('difficulty').max_length
        self.assertEqual(max_length, 20)

    # Verifies the string representation of a Recipe object is its name.
    def test_string_representation(self):
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(str(recipe), recipe.name)


