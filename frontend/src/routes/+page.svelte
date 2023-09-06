<script>
    import { Ingredient, Recipe } from '../models/recipeModel.js'; 
    
    let recipe = new Recipe();
    let ingredients = [new Ingredient()];
    let step = '';
    let steps = [];
    let note = '';
    let notes = [];
  
    function addIngredient() {
      ingredients.push(new Ingredient());
    }
  
    function addStep() {
      steps.push(step);
      step = '';
    }
  
    function addNote() {
      notes.push(note);
      note = '';
    }
  
    function handleSubmit() {
      recipe.ingredients = ingredients;
      recipe.steps = steps;
      recipe.notes = notes;
      
      // Here you'd send `recipe` to your server or directly to your MongoDB instance
      console.log(recipe);
    }
  </script>
  
  <h1>Create a New Recipe</h1>
  
  <form on:submit|preventDefault={handleSubmit}>
    <label>
      Recipe Name: 
      <input type="text" bind:value={recipe.recipeName} />
    </label>
  
    <label>
      Origin: 
      <input type="text" bind:value={recipe.origin} />
    </label>
  
    <label>
      Category: 
      <input type="text" bind:value={recipe.category} />
    </label>
  
    <label>
      Portion: 
      <input type="number" bind:value={recipe.portion} />
    </label>
  
    <h2>Ingredients</h2>
    {#each ingredients as ingredient, index}
      <div>
        <label>
          Name: 
          <input type="text" bind:value={ingredient.name} />
        </label>
        <label>
          Quantity: 
          <input type="number" bind:value={ingredient.quantity} />
        </label>
        <label>
          Unit: 
          <input type="text" bind:value={ingredient.unit} />
        </label>
      </div>
    {/each}
    <button type="button" on:click={addIngredient}>Add Another Ingredient</button>
  
    <h2>Steps</h2>
    {#each steps as step, index}
      <div>
        Step {index + 1}: {step}
      </div>
    {/each}
    <input type="text" bind:value={step} placeholder="Add a step..." />
    <button type="button" on:click={addStep}>Add Step</button>
  
    <h2>Notes</h2>
    {#each notes as note, index}
      <div>
        Note {index + 1}: {note}
      </div>
    {/each}
    <input type="text" bind:value={note} placeholder="Add a note..." />
    <button type="button" on:click={addNote}>Add Note</button>
  
    <button type="submit">Create Recipe</button>
  </form>
  