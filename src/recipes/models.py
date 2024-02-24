from django.db import models
from django.shortcuts import reverse

# Create your models here.

class Recipe(models.Model):
    name = models.CharField(max_length=50)
    ingredients = models.TextField()
    cooking_time = models.IntegerField()
    difficulty = models.CharField(max_length=20, blank=True)
    description = models.TextField()
    pic = models.ImageField(upload_to="recipes", default="no_picture")

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse ("recipes:detail", kwargs={"pk": self.pk})
    
    def return_ingredients_as_list(self):
        return self.ingredients.split(",")
    
    def calculate_difficulty(self):
        num_ingredients = len(self.return_ingredients_as_list())
        if self.cooking_time < 10 and num_ingredients < 4:
            return "Easy"
        elif self.cooking_time < 10 and num_ingredients >= 4:
            return "Medium"
        elif self.cooking_time >= 10 and num_ingredients < 4:
            return "Intermediate"
        elif self.cooking_time >= 10 and num_ingredients >= 4:
            return "Hard"
        
    def save(self, *args, **kwargs):
        self.difficulty = self.calculate_difficulty()
        super().save(*args, **kwargs)