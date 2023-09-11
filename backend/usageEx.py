# Usage example:

# Creating a Recipe instance
recipe = Recipe(
    "meatballs", 
    "mom", 
    "dinner", 
    2, 
    [Ingredient("carrot", 2, "kg"), Ingredient("potato", 2, "kg")], 
    ["description1", "description2"], 
    ["note1", "note2"]
)

# Convert the Recipe instance to JSON string
json_str = recipe.to_json()
print(json_str)

# Convert the JSON string back to a Recipe instance
new_recipe = Recipe.from_json(json_str)
print(new_recipe.__dict__)
