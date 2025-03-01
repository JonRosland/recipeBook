<script>
    import { onMount } from "svelte";
    import { recipeStore } from "../stores/RecipeStore.js";
    import { postRecipeApi, updateRecipeApi } from "./APIFunctions.js";

    export let isNewRecipe = true;
    export let recipeId = null;

    let saving = false;
    let currentRecipe = {};
    let errorMessage = "";

    onMount(() => {
        const unsubscribe = recipeStore.subscribe((recipe) => {
            currentRecipe = recipe;
            console.log("Current recipe from store:", currentRecipe);
        });

        return unsubscribe;
    });

    async function saveRecipe() {
        if (saving) return;

        saving = true;
        errorMessage = "";

        try {
            console.log("Saving recipe, isNewRecipe:", isNewRecipe);
            
            // Validate recipe data before sending
            if (!currentRecipe.recipeName && !currentRecipe.title) {
                throw new Error("Recipe name is required");
            }

            // Create a deep copy of the recipe to modify for the API
            const apiRecipe = JSON.parse(JSON.stringify(currentRecipe));
            
            // Ensure title is set (backend expects title, frontend uses recipeName)
            if (!apiRecipe.title && apiRecipe.recipeName) {
                apiRecipe.title = apiRecipe.recipeName;
            }

            // Make ingredients an empty array if it's undefined
            if (!apiRecipe.ingredients) {
                apiRecipe.ingredients = [];
            }

            // Make steps an empty array if it's undefined
            if (!apiRecipe.steps) {
                apiRecipe.steps = [];
            }

            console.log("Recipe prepared for API:", apiRecipe);

            if (isNewRecipe) {
                // Create new recipe
                console.log("Creating new recipe");
                const response = await postRecipeApi(apiRecipe);
                console.log("Create recipe response:", response);
                
                if (response && response.recipe_id) {
                    alert("Oppskrift lagret!");
                    window.location.href = `/recipe/${response.recipe_id}`;
                } else {
                    throw new Error("Failed to create recipe - no recipe ID returned");
                }
            } else if (recipeId) {
                // Update existing recipe
                console.log(`Updating recipe with ID: ${recipeId}`);
                const response = await updateRecipeApi(recipeId, apiRecipe);
                console.log("Update recipe response:", response);
                
                alert("Oppskrift oppdatert!");
                window.location.href = `/recipe/${recipeId}`;
            }
        } catch (error) {
            console.error("Error saving recipe:", error);
            errorMessage = `Feil ved lagring av oppskrift: ${error.message}`;
            alert("Feil ved lagring av oppskrift. Vennligst prøv igjen.");
        } finally {
            saving = false;
        }
    }
</script>

{#if errorMessage}
    <div class="error-message">{errorMessage}</div>
{/if}

<button
    class="save-button"
    on:click={saveRecipe}
    disabled={saving}
    aria-label="Save recipe"
>
    {#if saving}
        <span class="saving-indicator"></span>
    {:else}
        <svg
            class="save-icon"
            viewBox="0 0 24 24"
            stroke="var(--icon-color)"
            stroke-width="2"
            fill="none"
        >
            <path
                d="M19 21H5a2 2 0 01-2-2V5a2 2 0 012-2h11l5 5v11a2 2 0 01-2 2z"
            ></path>
            <polyline points="17 21 17 13 7 13 7 21"></polyline>
            <polyline points="7 3 7 8 15 8"></polyline>
        </svg>
    {/if}
</button>

<style>
    .save-button {
        position: fixed;
        bottom: var(--spacing-xxl);
        right: var(--spacing-xxl);
        width: 70px;
        height: 70px;
        border-radius: 50%;
        background-color: var(--primary-color);
        border: none;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: var(--floating-button-shadow);
        z-index: 100;
    }

    .save-button:disabled {
        opacity: 0.7;
        cursor: not-allowed;
    }

    .save-icon {
        width: 32px;
        height: 32px;
        stroke: var(--icon-color);
        stroke-width: 2;
        fill: none;
    }

    .saving-indicator {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        border: 3px solid rgba(255, 255, 255, 0.3);
        border-top-color: #2c4658;
        animation: spin 1s infinite linear;
    }

    .error-message {
        position: fixed;
        bottom: calc(var(--spacing-xxl) * 2 + 70px);
        right: var(--spacing-xxl);
        background-color: #ffebee;
        color: #d32f2f;
        padding: var(--spacing-sm) var(--spacing-md);
        border-radius: var(--border-radius);
        box-shadow: var(--card-shadow);
        z-index: 100;
        max-width: 300px;
    }

    @keyframes spin {
        to {
            transform: rotate(360deg);
        }
    }
</style>