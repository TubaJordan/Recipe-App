from .models import Recipe
from collections import Counter
from io import BytesIO
import base64
import matplotlib.pyplot as plt


def get_graph():
    # Converts the current matplotlib plot into a PNG image encoded in base64.
    buffer = BytesIO() # Create a buffer in memory to store the image.
    plt.savefig(buffer, format='png', transparent=True) # Save the current matplotlib figure to the buffer as a PNG.
    buffer.seek(0) # Move to the beginning of the buffer to read its contents.
    image_png = buffer.getvalue() # Read the image data from the buffer.
    graph = base64.b64encode(image_png) # Encode the binary image data to base64.
    graph = graph.decode('utf-8') # Decode the base64-encoded data into a string.
    buffer.close() # Close the buffer.
    return graph # Return the base64-encoded image string.


def get_popular_ingredients_chart(recipes):
    # Generates a bar chart of the most popular ingredients across a list of recipes.
    all_ingredients = [] # Initialize a list to hold all ingredients from all recipes.
    # Extract ingredients from each recipe and normalize them.
    for recipe in recipes:
        ingredients_list = recipe['ingredients'].split(',') # Split the ingredients string into a list.
        normalized = [ingredient.strip().lower() for ingredient in ingredients_list] # Normalize ingredients to lowercase and strip whitespace.
        all_ingredients.extend(normalized) # Add the normalized ingredients to the list of all ingredients.
    
    ingredient_counts = Counter(all_ingredients) # Count occurrences of each ingredient.
    # Get the 10 most common ingredients and their counts.
    ingredients, counts = zip(*ingredient_counts.most_common(10)) if all_ingredients else ([], [])
    
    plt.switch_backend('AGG')  # Use the 'agg' backend for headless environments.
    plt.figure(figsize=(10, 6)) # Set the figure size.

    # Create the bar chart if there are ingredients and counts.
    if ingredients and counts:
        plt.bar(ingredients, counts, color='maroon') # Plot the bar chart.
        plt.xlabel('Ingredients') # Label the x-axis.
        plt.ylabel('Number of Recipes') # Label the y-axis.
        plt.title('Most Popular Ingredients') # Set the chart title.
        plt.xticks(rotation=45) # Rotate x-axis labels for better readability.
    else:
        # Display a message if there is no data.
        plt.text(0.5, 0.5, 'No data available', horizontalalignment='center', verticalalignment='center')
    plt.tight_layout() # Adjust layout to not overlap.
    
    chart = get_graph() # Convert the plot to a base64-encoded image.
    plt.close() # Close the matplotlib figure to free memory.
    return chart # Return the base64-encoded image.


def get_recipe_distribution_by_difficulty_chart(recipes):
    # Generates a pie chart showing the distribution of recipes by difficulty.
    # Count recipes by difficulty.
    difficulty_distribution = Counter(recipe['difficulty'] for recipe in recipes if 'difficulty' in recipe)
    
    plt.switch_backend('AGG') # Use the 'agg' backend.
    plt.figure(figsize=(8, 8)) # Set figure size.
    # Plot the pie chart if there is data.
    if difficulty_distribution:
        plt.pie(difficulty_distribution.values(), labels=difficulty_distribution.keys(), autopct='%1.1f%%', startangle=140)
        plt.title('Recipe Distribution by Difficulty') # Set title.
        plt.axis('equal')  # Ensure the pie chart is circular.
    else:
        # Display a message if there is no data.
        plt.text(0.5, 0.5, 'No data available', horizontalalignment='center', verticalalignment='center', fontsize=12)
    plt.tight_layout() # Adjust layout.
    
    chart = get_graph() # Convert the plot to a base64-encoded image.
    plt.close() # Close the figure.
    return chart # Return the image.


def get_cooking_time_by_difficulty_chart(recipes):
    # Generates a line chart showing average cooking time by difficulty level.
    # Organize recipes by difficulty and collect their cooking times.
    difficulty_levels = ['Easy', 'Medium', 'Intermediate', 'Hard']
    cooking_times = {difficulty: [] for difficulty in difficulty_levels}

    for recipe in recipes:
        if recipe['difficulty'] in cooking_times:
            cooking_times[recipe['difficulty']].append(recipe['cooking_time'])
    
    # Calculate average cooking time for each difficulty level.
    avg_cooking_times = {difficulty: sum(times)/len(times) if times else 0 for difficulty, times in cooking_times.items()}

    plt.switch_backend('AGG') # Use the 'agg' backend.
    plt.figure(figsize=(10, 6)) # Set figure size.
    # Plot the line chart.
    plt.plot(list(avg_cooking_times.keys()), list(avg_cooking_times.values()), marker='o', linestyle='-', color='blue')
    plt.title('Average Cooking Time by Difficulty') # Set title.
    plt.xlabel('Difficulty Level') # Label x-axis.
    plt.ylabel('Average Cooking Time (minutes)') # Label y-axis.
    plt.grid(True) # Add a grid for readability.
    plt.tight_layout() # Adjust layout.

    chart = get_graph() # Convert the plot to a base64-encoded image.
    plt.close() # Close the figure.
    return chart # Return the image.