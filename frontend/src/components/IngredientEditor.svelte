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

    <!-- Desktop and mobile layouts -->
    <div class="form-layout">
        <!-- Ingredient name (always full width) -->
        <input
            type="text"
            class="input-field name-input"
            placeholder="Ingrediens"
            bind:value={newIngredient.name}
        />
        
        <!-- This container handles the responsive behavior -->
        <div class="inputs-container">
            <!-- Quantity and unit will be side by side on all screens -->
            <div class="unit-quantity-row">
                <input
                    type="number"
                    class="input-field quantity-input"
                    placeholder="Mengde"
                    bind:value={newIngredient.quantity}
                />
                <input
                    type="text"
                    class="input-field unit-input"
                    placeholder="Enhet"
                    bind:value={newIngredient.unit}
                />
            </div>
            
            <!-- Button - shares row on desktop, own row on mobile -->
            <button class="btn add-btn" on:click={addIngredient}>
                Legg til Ingrediens
            </button>
        </div>
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

    .form-layout {
        display: flex;
        flex-direction: column;
        gap: var(--spacing-md);
    }
    
    .input-field {
        background-color: var(--input-background);
        border: none;
        border-radius: var(--input-radius);
        padding: 12px 15px;
        font-size: 16px;
        height: 45px;
        box-sizing: border-box;
    }

    .input-field::placeholder {
        color: var(--text-light);
    }

    /* Reset browser-specific styling for number inputs */
    input[type="number"] {
        -moz-appearance: textfield; /* Firefox */
    }

    input[type="number"]::-webkit-inner-spin-button,
    input[type="number"]::-webkit-outer-spin-button {
        -webkit-appearance: none;
        margin: 0;
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
        box-sizing: border-box;
    }
    
    /* Name input is always full width */
    .name-input {
        width: 100%;
        margin-bottom: var(--spacing-md);
    }
    
    /* Container for the bottom inputs */
    .inputs-container {
        display: flex;
        gap: var(--spacing-md);
    }
    
    /* Grid for quantity and unit */
    .unit-quantity-row {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: var(--spacing-md);
        flex: 2;
    }
    
    /* Ensure inputs take full width of their grid cell */
    .quantity-input, .unit-input {
        width: 100%;
        min-width: 0; /* Prevent overflow issues */
    }
    
    /* Button styling */
    .add-btn {
        flex: 1;
    }

    /* List styles remain the same */
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

    /* Mobile layout */
    @media (max-width: 640px) {
        .inputs-container {
            flex-direction: column;
        }
        
        .unit-quantity-row {
            width: 100%;
            display: flex; /* Changed to flexbox for better control */
            gap: var(--spacing-md);
            flex: none; /* Reset the flex property from desktop */
        }
        
        .quantity-input, .unit-input {
            flex: 1; /* Each input takes equal space */
            min-width: 0; /* Prevent content from causing overflow */
        }
        
        .add-btn {
            width: 100%;
            margin-top: 5px;
        }
    }
</style>