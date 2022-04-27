import requests
import json
from models import RecipeModel, RecipeNutritionModel, RecipeIngredientsModel
# Website URL (docs): https://rapidapi.com/edamam/api/recipe-search-and-diet/
# Website URL (docs): https://rapidapi.com/edamam/api/edamam-nutrition-analysis/

"""
url = "https://edamam-recipe-search.p.rapidapi.com/search"
params = {"q": "Vegetarian Chicken Sandwich"}       # Search literally any recipe/food type (string).

headers = {
	"X-RapidAPI-Host": "edamam-recipe-search.p.rapidapi.com",
	"X-RapidAPI-Key": "a5b0806962mshe36b0ed1b7175d5p152becjsnc7ea3913781c"
}

response = requests.get(url, headers=headers, params=params)
"""

json_response: str
with open('recipesResponse.txt', 'r') as f:
    json_response = f.read()

# Get the JSON Response as a Dictionary Object.
data = json.loads(json_response)

# Lets iterate through the Top 5 Recipe results and gather data for each Recipe returned.
results: list[RecipeModel] = []
for index in range(5):
    raw_results = data["hits"][index]["recipe"]
    ingredients = [RecipeIngredientsModel(ingredient["text"], ingredient["image"]) for ingredient in raw_results["ingredients"]]
    total_nutrition = RecipeNutritionModel(raw_results["totalNutrients"])

    results.append(RecipeModel(raw_results["label"], raw_results["cuisineType"], raw_results["shareAs"], raw_results["yield"], ingredients, total_nutrition))

for recipe in results:
    print(recipe.report_recipe_data())