from .models import Recipe
from collections import Counter
from io import BytesIO
import base64
import matplotlib.pyplot as plt



def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png', transparent=True)
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def get_popular_ingredients_chart(recipes):
    all_ingredients = []
    for recipe in recipes:
        ingredients_list = recipe['ingredients'].split(',')
        normalized = [ingredient.strip().lower() for ingredient in ingredients_list]
        all_ingredients.extend(normalized)
    
    ingredient_counts = Counter(all_ingredients)
    ingredients, counts = zip(*ingredient_counts.most_common(10)) if all_ingredients else ([], [])
    
    plt.switch_backend('AGG')  # Use the 'agg' backend for rendering
    plt.figure(figsize=(10, 6))

    if ingredients and counts:
        plt.bar(ingredients, counts, color='maroon')
        plt.xlabel('Ingredients')
        plt.ylabel('Number of Recipes')
        plt.title('Most Popular Ingredients')
        plt.xticks(rotation=45)
    else:
        plt.text(0.5, 0.5, 'No data available', horizontalalignment='center', verticalalignment='center')
    plt.tight_layout()
    
    chart = get_graph()
    plt.close()
    return chart


def get_recipe_distribution_by_difficulty_chart(recipes):
    difficulty_distribution = Counter(recipe['difficulty'] for recipe in recipes if 'difficulty' in recipe)
    
    plt.switch_backend('AGG')
    plt.figure(figsize=(8, 8))
    if difficulty_distribution:
        plt.pie(difficulty_distribution.values(), labels=difficulty_distribution.keys(), autopct='%1.1f%%', startangle=140)
        plt.title('Recipe Distribution by Difficulty')
        plt.axis('equal')  # Ensure pie chart is a circle
    else:
        plt.text(0.5, 0.5, 'No data available', horizontalalignment='center', verticalalignment='center', fontsize=12)
    plt.tight_layout()
    
    chart = get_graph()
    plt.close()
    return chart


def get_cooking_time_by_difficulty_chart(recipes):
    # Organize recipes by difficulty
    difficulty_levels = ['Easy', 'Medium', 'Intermediate', 'Hard']
    cooking_times = {difficulty: [] for difficulty in difficulty_levels}

    for recipe in recipes:
        if recipe['difficulty'] in cooking_times:
            cooking_times[recipe['difficulty']].append(recipe['cooking_time'])
    
    # Calculate average cooking time for each difficulty
    avg_cooking_times = {difficulty: sum(times)/len(times) if times else 0 for difficulty, times in cooking_times.items()}

    # Plotting
    plt.switch_backend('AGG')
    plt.figure(figsize=(10, 6))
    plt.plot(list(avg_cooking_times.keys()), list(avg_cooking_times.values()), marker='o', linestyle='-', color='blue')
    plt.title('Average Cooking Time by Difficulty')
    plt.xlabel('Difficulty Level')
    plt.ylabel('Average Cooking Time (minutes)')
    plt.grid(True)
    plt.tight_layout()

    chart = get_graph()
    plt.close()
    return chart