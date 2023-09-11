import json

class Recipe:
    def __init__(self, recipe_name, origin, category, portion, ingredients, steps, notes):
        self.recipe_name = recipe_name
        self.origin = origin
        self.category = category
        self.portion = portion
        self.ingredients = ingredients
        self.steps = steps
        self.notes = notes

    def to_json(self):
        return json.dumps(self.__dict__, default=lambda o: o.__dict__, indent=4)

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        ingredients = [Ingredient(**item) for item in data['ingredients']]
        return cls(data['recipe_name'], data['origin'], data['category'], data['portion'], ingredients, data['steps'], data['notes'])

class Ingredient:
    def __init__(self, name, quantity, unit):
        self.name = name
        self.quantity = quantity
        self.unit = unit


