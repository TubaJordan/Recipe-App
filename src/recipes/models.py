from django.db import models
from django.shortcuts import reverse
from django.core.validators import MinValueValidator
from django.conf import settings
import os


class Recipe(models.Model):
    # Define fields for the Recipe model.
    name = models.CharField(max_length=50) # Recipe name field with a maximum length of 50 characters.
    ingredients = models.TextField() # Ingredients list stored as text.
    cooking_time = models.IntegerField(validators=[MinValueValidator(0)]) # Cooking time in minutes, stored as an integer.
    difficulty = models.CharField(max_length=20, blank=True) # Difficulty level of the recipe, optional field.
    description = models.TextField() # Detailed description of the recipe.
    pic = models.ImageField(upload_to="recipes", default="no_picture") # Image for the recipe with a default image if none is uploaded.

    def __str__(self):
        return self.name # Return the name of the recipe when it's represented as a string.
    
    def get_absolute_url(self):
        return reverse ("recipes:detail", kwargs={"pk": self.pk}) # Generate the URL for a recipe's detail view using its primary key (pk).
    
    def return_ingredients_as_list(self):
        return self.ingredients.split(",") # Split the ingredients field by commas and return as a list.
    
    def calculate_difficulty(self):
        # Determine the recipe's difficulty based on cooking time and number of ingredients.
        num_ingredients = len(self.return_ingredients_as_list()) # Count the number of ingredients.
        if self.cooking_time < 10 and num_ingredients < 4:
            return "Easy"
        elif self.cooking_time < 10 and num_ingredients >= 4:
            return "Medium"
        elif self.cooking_time >= 10 and num_ingredients < 4:
            return "Intermediate"
        elif self.cooking_time >= 10 and num_ingredients >= 4:
            return "Hard"
        
    def save(self, *args, **kwargs):
        self.difficulty = self.calculate_difficulty() # Set the difficulty level before saving.
        super().save(*args, **kwargs) # Call the parent class's save method to handle saving the instance.
      
    def delete(self, *args, **kwargs):
        # Check for an associated image and if it's not the default
        if self.pic and not self.pic.name == "no_picture":
            # Get the path to the image
            img_path = self.pic.path
            if os.path.isfile(img_path):
                # Delete the file if it exists
                os.remove(img_path)
        super().delete(*args, **kwargs)  # Call the super class's delete method