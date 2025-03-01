<script>
    import { onMount } from "svelte";
    import {
        recipeStore,
        updateRecipeStore,
        deleteElementStore,
        swapElementsStore,
    } from "../stores/RecipeStore.js";

    export let ingredients = [];

    let newIngredient = { name: "", quantity: "", unit: "" };
    let recipeIngredients = [];

    onMount(() => {
        if (ingredients && ingredients.length > 0) {
            // Initialize with provided ingredients if available
            recipeIngredients = [...ingredients];
        }

        // Subscribe to store changes
        const unsubscribe = recipeStore.subscribe((recipe) => {
            recipeIngredients = recipe.ingredients || [];
        });

        return unsubscribe;
    });

    function addIngredient() {
        if (newIngredient.name) {
            // Make sure quantity is a number
            const quantity =
                newIngredient.quantity === ""
                    ? 0
                    : parseFloat(newIngredient.quantity);

            const ingredient = {
                name: newIngredient.name,
                quantity: quantity,
                unit: newIngredient.unit,
            };

            updateRecipeStore("ingredients", ingredient);

            // Reset the form
            newIngredient = { name: "", quantity: "", unit: "" };
        }
    }

    function moveIngredient(index, direction) {
        const newIndex = index + direction;
        if (newIndex >= 0 && newIndex < recipeIngredients.length) {
            swapElementsStore("ingredients", index, newIndex);
        }
    }

    function removeIngredient(index) {
        deleteElementStore("ingredients", index);
    }
</script>

<section class="section-card">
    <h3 class="section-title">Ingredienser</h3>

    <div class="form-row">
        <input
            type="text"
            class="input-field"
            placeholder="Ingrediens"
            bind:value={newIngredient.name}
        />
    </div>

    <div class="form-row ingredient-row">
        <input
            type="number"
            class="input-field ingredient-quantity"
            placeholder="Mengde"
            bind:value={newIngredient.quantity}
        />
        <input
            type="text"
            class="input-field ingredient-unit"
            placeholder="Enhet"
            bind:value={newIngredient.unit}
        />
        <button class="btn" on:click={addIngredient}>Legg til Ingrediens</button
        >
    </div>

    <div class="item-list">
        {#each recipeIngredients as ingredient, index}
            <div class="list-item">
                <div class="list-bullet">•</div>
                <div class="list-item-content">
                    {ingredient.name}
                    {ingredient.quantity}
                    {ingredient.unit}
                </div>
                <div class="action-buttons">
                    <button
                        class="action-btn"
                        on:click={() => moveIngredient(index, 1)}
                        aria-label="Move down"
                        disabled={index === recipeIngredients.length - 1}
                    >
                        <svg
                            class="action-icon"
                            viewBox="0 0 24 24"
                            stroke="var(--text-on-primary)"
                            stroke-width="2"
                            fill="none"
                        >
                            <polyline points="6 9 12 15 18 9"></polyline>
                        </svg>
                    </button>
                    <button
                        class="action-btn"
                        on:click={() => moveIngredient(index, -1)}
                        aria-label="Move up"
                        disabled={index === 0}
                    >
                        <svg
                            class="action-icon"
                            viewBox="0 0 24 24"
                            stroke="var(--text-on-primary)"
                            stroke-width="2"
                            fill="none"
                        >
                            <polyline points="18 15 12 9 6 15"></polyline>
                        </svg>
                    </button>
                    <button
                        class="action-btn"
                        on:click={() => removeIngredient(index)}
                        aria-label="Delete"
                    >
                        <svg
                            class="action-icon"
                            viewBox="0 0 24 24"
                            stroke="var(--text-on-primary)"
                            stroke-width="2"
                            fill="none"
                        >
                            <polyline points="3 6 5 6 21 6"></polyline>
                            <path
                                d="M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2"
                            ></path>
                        </svg>
                    </button>
                </div>
            </div>
        {/each}
    </div>
</section>

<style>
    .section-card {
        background-color: var(--card-background);
        border-radius: var(--card-radius);
        box-shadow: var(--card-shadow);
        padding: var(--spacing-xl);
        margin-bottom: var(--spacing-xl);
    }

    .section-title {
        color: var(--primary-color);
        font-size: 28px;
        margin-bottom: var(--spacing-lg);
        font-weight: 500;
    }

    .form-row {
        display: flex;
        gap: var(--spacing-md);
        margin-bottom: var(--spacing-md);
        align-items: stretch;
    }

    .input-field {
        background-color: var(--input-background);
        border: none;
        border-radius: var(--input-radius);
        padding: 12px 15px;
        font-size: 16px;
        flex-grow: 1;
        height: 45px;
    }

    .input-field::placeholder {
        color: var(--text-light);
    }

    .btn {
        background-color: var(--primary-color, #55a7ac);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 15px;
        font-size: 16px;
        cursor: pointer;
        text-align: center;
        height: 45px;
        width: 180px;
        flex-shrink: 0;
    }

    .ingredient-row {
        display: flex;
        gap: 10px;
    }

    .ingredient-quantity {
        width: 120px;
        flex-shrink: 1;
        flex-grow: 0;
    }

    .ingredient-unit {
        width: 150px;
        flex-shrink: 1;
        flex-grow: 0;
    }

    .item-list {
        margin-top: 20px;
    }

    .list-item {
        display: flex;
        align-items: flex-start;
        margin-bottom: 15px;
    }

    .list-item-content {
        flex-grow: 1;
        padding-left: 10px;
        padding-right: 10px;
        word-break: break-word;
    }

    .action-buttons {
        display: flex;
        gap: 5px;
    }

    .action-btn {
        width: 40px;
        height: 40px;
        border-radius: 5px;
        border: none;
        background-color: var(--primary-color, #55a7ac);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
    }

    .action-btn:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }

    .action-icon {
        width: 20px;
        height: 20px;
        stroke: white;
        stroke-width: 2;
        fill: none;
    }

    .list-bullet {
        min-width: 20px;
        padding-top: 2px;
    }
</style>
