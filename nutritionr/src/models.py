from django.db import models

# Create your models here.
class IngredientsModel:
    """ A class for the Nutrients section for any searched consumable. """
    pk: str
    label: str
    calories: float
    protein: float
    fat: float
    fiber: float
    image_uri: str

    def __init__(self, pk, label, calories: float, protein, fat, fiber, image_uri):
        self.pk = pk
        self.label = label
        self.calories = calories
        self.protein = protein
        self.fat = fat
        self.fiber = fiber
        self.image_uri = image_uri

class RecipeIngredientsModel:
    """ Model for storing an ingredient and an image of it derived from a Recipe. """
    label: str
    image_uri: str

    def __init__(self, label, image_uri):
        self.label = label
        self.image_uri = image_uri

class RecipeNutritionModel:
    """ Model for storing total nutritional info for a given Recipe. """
    # These metrics will be strings formatted like so: {count} {unit}
    calories: float
    protein: str
    total_fat: str
    carbs: str
    fiber: str
    sugar: str
    sugar_added: str
    cholesterol: str
    sodium: str
    calcium: str
    potassium: str
    iron: str

    def __init__(self, json_data, servings: int):
        """ Default constructor that assigns the values of this class' members from JSON data. """
        self.calories = float(json_data["ENERC_KCAL"]["quantity"])/float(servings)
        self.protein = f'{float(json_data["PROCNT"]["quantity"])/float(servings):.2f}{json_data["PROCNT"]["unit"]}' if json_data.get("PROCNT") else 'No Data Found'
        self.total_fat = f'{float(json_data["FAT"]["quantity"])/float(servings):.2f}{json_data["FAT"]["unit"]}' if json_data.get("FAT") else 'No Data Found'
        self.carbs = f'{float(json_data["CHOCDF"]["quantity"])/float(servings):.2f}{json_data["CHOCDF"]["unit"]}' if json_data.get("CHOCDF") else 'No Data Found'
        self.fiber = f'{float(json_data["FIBTG"]["quantity"])/float(servings):.2f}{json_data["FIBTG"]["unit"]}' if json_data.get("FIBTG") else 'No Data Found'
        self.sugar = f'{float(json_data["SUGAR"]["quantity"])/float(servings):.2f}{json_data["SUGAR"]["unit"]}' if json_data.get("SUGAR") else 'No Data Found'
        self.sugar_added = f'{float(json_data["SUGAR.added"]["quantity"])/float(servings):.2f}{json_data["SUGAR.added"]["unit"]}' if json_data.get("SUGAR.added") else 'No Data Found'
        self.cholesterol = f'{float(json_data["CHOLE"]["quantity"])/float(servings):.2f}{json_data["CHOLE"]["unit"]}' if json_data.get("CHOLE") else 'No Data Found'
        self.sodium = f'{float(json_data["NA"]["quantity"])/float(servings):.2f}{json_data["NA"]["unit"]}' if json_data.get("NA") else 'No Data Found'
        self.calcium = f'{float(json_data["CA"]["quantity"])/float(servings):.2f}{json_data["CA"]["unit"]}' if json_data.get("CA") else 'No Data Found'
        self.potassium = f'{float(json_data["K"]["quantity"])/float(servings):.2f}{json_data["K"]["unit"]}' if json_data.get("K") else 'No Data Found'
        self.iron = f'{float(json_data["FE"]["quantity"])/float(servings):.2f}{json_data["FE"]["unit"]}' if json_data.get("FE") else 'No Data Found'

class RecipeModel:
    """ Model for handling the data for recipes, its ingredients, and its nutritional facts. """
    pk: str
    label: str
    cuisine_type: str
    share_as_uri: str
    servings_yield: float
    ingredients: list[RecipeIngredientsModel]
    nutrition: RecipeNutritionModel
    nutrition_serving: RecipeNutritionModel
    nutrition_daily: RecipeNutritionModel
    nutrition_daily_serving: RecipeNutritionModel

    def __init__(self, pk, label, cuisine_type, share_as_uri, servings_yield, ingredients, nutrition, nutrition_serving, nutrition_daily, nutrition_daily_serving):
        self.pk = pk
        self.label = label
        self.cuisine_type = cuisine_type
        self.share_as_uri = share_as_uri
        self.servings_yield = servings_yield
        self.ingredients = ingredients
        self.nutrition = nutrition
        self.nutrition_serving = nutrition_serving
        self.nutrition_daily = nutrition_daily
        self.nutrition_daily_serving = nutrition_daily_serving
        