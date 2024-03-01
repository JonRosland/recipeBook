<script>
    export let recipe = {
        recipeName: "recipeName",
        origin: "Origin",
        category: "Category",
        portion: 0,
        region: "region",
        ingredients: [],
        steps: [],
        notes: [],
    };

    let portionModifier = 0;

    function handlePlus() {
        portionModifier += 1;
    }
    function handleMinus() {
        portionModifier -= 1;
    }
</script>

<section class="ingredients">
    <h4>
        Porsjoner: {portionModifier + recipe.portion}
        <button
            on:click={handleMinus}
            style="border: 2px solid black; padding: 5px 10px;">-</button
        >
        <button
            on:click={handlePlus}
            style="border: 2px solid black; padding: 5px 10px;">+</button
        >
    </h4>
    <h2>Ingredienser</h2>
    <div class="ingredient">
        <ul>
            {#each recipe.ingredients as ingredient}
                <li>
                    {ingredient.name}
                    {ingredient.quantity * (portionModifier + recipe.portion)}
                    {ingredient.unit}
                </li>
            {/each}
        </ul>
    </div>
</section>

<style>
    .ingredients {
        grid-area: i;
    }

    .ingredient {
        text-align: left;
    }

    section {
        border: 1px solid black;
        margin: 0 1em 1em 0;
        padding: 1em;
        box-sizing: border-box;
        flex: 2 1 40%; /* Grow to 40% of the container's width */
        min-width: 300px; /* Minimum width before wrapping */
    }

    ul {
        list-style: none;
        padding: 0;
    }
</style>
