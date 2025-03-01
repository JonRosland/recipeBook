<script>
    import { onMount } from "svelte";
    import { recipeStore } from "../stores/RecipeStore.js";
    import { postRecipeApi, updateRecipeApi } from "./APIFunctions.js";

    export let isNewRecipe = true;
    export let recipeId = null;

    let saving = false;
    let currentRecipe = {};

    onMount(() => {
        const unsubscribe = recipeStore.subscribe((recipe) => {
            currentRecipe = recipe;
        });

        return unsubscribe;
    });

    async function saveRecipe() {
        if (saving) return;

        saving = true;

        try {
            if (isNewRecipe) {
                // Create new recipe
                const response = await postRecipeApi(currentRecipe);
                if (response && response.recipe_id) {
                    alert("Oppskrift lagret!");
                    window.location.href = `/recipe/${response.recipe_id}`;
                } else {
                    throw new Error("Failed to create recipe");
                }
            } else if (recipeId) {
                // Update existing recipe
                await updateRecipeApi(recipeId, currentRecipe);
                alert("Oppskrift oppdatert!");
                window.location.href = `/recipe/${recipeId}`;
            }
        } catch (error) {
            console.error("Error saving recipe:", error);
            alert("Feil ved lagring av oppskrift. Vennligst prøv igjen.");
        } finally {
            saving = false;
        }
    }
</script>

<button
    class="save-button"
    on:click={saveRecipe}
    disabled={saving}
    aria-label="Save recipe"
>
    {#if saving}
        <span class="saving-indicator"></span>
    {:else}
        <svg class="save-icon" viewBox="0 0 24 24">
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
        stroke: var(--primary-color-dark);
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

    @keyframes spin {
        to {
            transform: rotate(360deg);
        }
    }
</style>
