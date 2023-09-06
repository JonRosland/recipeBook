export class Ingredient {
  constructor(name = "", quantity = 0, unit = "") {
    this.name = name;
    this.quantity = quantity;
    this.unit = unit;
  }
}

export class Recipe {
  constructor(
    recipeName = "", 
    origin = "", 
    category = "", 
    portion = 0, 
    ingredients = [], 
    steps = [], 
    notes = []
  ) {
    this.recipeName = recipeName;
    this.origin = origin;
    this.category = category;
    this.portion = portion;
    this.ingredients = ingredients; 
    this.steps = steps;
    this.notes = notes;
  }
}
