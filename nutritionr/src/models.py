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

    def report_nutrient_data(self):
        """ Write out the results gathered for this item. """
        return f"""
        '{self.label}' Nutritional Facts:
            >>> Calories:   {self.calories}
            >>> Protein:    {self.protein}g
            >>> Fat:        {self.fat}g
            >>> Fiber:      {self.fiber}g
        """

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

    def __init__(self, json_data):
        """ Default constructor that assigns the values of this class' members from JSON data. """
        self.calories = float(json_data["ENERC_KCAL"]["quantity"])
        self.protein = f'{float(json_data["PROCNT"]["quantity"]):.2f}{json_data["PROCNT"]["unit"]}'
        self.total_fat = f'{float(json_data["FAT"]["quantity"]):.2f}{json_data["FAT"]["unit"]}'
        self.carbs = f'{float(json_data["CHOCDF"]["quantity"]):.2f}{json_data["CHOCDF"]["unit"]}'
        self.fiber = f'{float(json_data["FIBTG"]["quantity"]):.2f}{json_data["FIBTG"]["unit"]}'
        self.sugar = f'{float(json_data["SUGAR"]["quantity"]):.2f}{json_data["SUGAR"]["unit"]}'
        self.sugar_added = f'{float(json_data["SUGAR.added"]["quantity"]):.2f}{json_data["SUGAR.added"]["unit"]}'
        self.cholesterol = f'{float(json_data["CHOLE"]["quantity"]):.2f}{json_data["CHOLE"]["unit"]}'
        self.sodium = f'{float(json_data["NA"]["quantity"]):.2f}{json_data["NA"]["unit"]}'
        self.calcium = f'{float(json_data["CA"]["quantity"]):.2f}{json_data["CA"]["unit"]}'
        self.potassium = f'{float(json_data["K"]["quantity"]):.2f}{json_data["K"]["unit"]}'
        self.iron = f'{float(json_data["FE"]["quantity"]):.2f}{json_data["FE"]["unit"]}'

class RecipeModel:
    """ Model for handling the data for recipes, its ingredients, and its nutritional facts. """
    label: str
    cuisine_type: str
    share_as_uri: str
    servings_yield: float
    ingredients: list[RecipeIngredientsModel]
    nutrition: RecipeNutritionModel

    def __init__(self, label, cuisine_type, share_as_uri, servings_yield, ingredients, nutrition):
        self.label = label
        self.cuisine_type = cuisine_type
        self.share_as_uri = share_as_uri
        self.servings_yield = servings_yield
        self.ingredients = ingredients
        self.nutrition = nutrition
    
    def report_recipe_data(self):
        return f"""
            Recipe Name:        {self.label}
            Cuisine Type:       {self.cuisine_type}
            Servings Yield:     {self.servings_yield}
            Ingredients:        {[ingredient.label for ingredient in self.ingredients]}

            Total Nutrition Facts:
            Calories/Serving:   {(self.nutrition.calories / self.servings_yield):.2f}
            Protein:            {self.nutrition.protein}
            Total Fats:         {self.nutrition.total_fat}
            Carbs:              {self.nutrition.carbs}

            Share this recipe via: {self.share_as_uri}
        """