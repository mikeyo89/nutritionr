import requests
import json
from models import IngredientsModel

# Website URL (docs): https://rapidapi.com/edamam/api/edamam-food-and-grocery-database/

"""
# Get API response data for specified consumable.
url = "https://edamam-food-and-grocery-database.p.rapidapi.com/parser"
querystring = {"ingr":"apple"}

headers = {
	"X-RapidAPI-Host": "edamam-food-and-grocery-database.p.rapidapi.com",
	"X-RapidAPI-Key": "a5b0806962mshe36b0ed1b7175d5p152becjsnc7ea3913781c"
}

response = requests.get(url, headers=headers, params=querystring)
"""

with open('ingredientsResponse.txt', 'r') as f:
    response = f.read()

# Get top 5 results of items for search term 'apple'
data = json.loads(response)['hints']
results: list[IngredientsModel] = []
for x in range(5):
    raw_nutrients = data[x]['food']['nutrients']
    result = IngredientsModel(data[x]['food']['label'], raw_nutrients['ENERC_KCAL'], raw_nutrients['PROCNT'], raw_nutrients['FAT'], raw_nutrients['FIBTG'])
    results.append(result)

# Print out results.
for result in results:
    print(result.report_nutrient_data())