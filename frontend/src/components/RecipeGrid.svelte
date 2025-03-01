<script>
    import { onMount } from "svelte";
    import RecipeCard from "./RecipeCard.svelte";
    import { searchResults, hasSearched } from "../stores/SearchStore.js";

    export let recipes = [];
    let displayedRecipes = [];

    onMount(() => {
        // Initialize with all recipes
        displayedRecipes = recipes;

        // Subscribe to search results
        const unsubscribe = searchResults.subscribe((results) => {
            if (results.length > 0) {
                displayedRecipes = results;
            } else {
                displayedRecipes = recipes;
            }
        });

        return unsubscribe;
    });
</script>

<div class="recipe-grid">
    {#if displayedRecipes && displayedRecipes.length > 0}
        {#each displayedRecipes as recipe (recipe._id)}
            <RecipeCard {recipe} />
        {/each}
    {:else}
        <div class="no-results">
            <p>Ingen oppskrifter funnet.</p>
        </div>
    {/if}
</div>

<style>
    .recipe-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
        margin-bottom: 100px;
    }

    .no-results {
        grid-column: 1 / -1;
        text-align: center;
        padding: 40px;
        color: var(--primary-color, #55a7ac);
        font-size: 24px;
    }

    @media (max-width: 768px) {
        .recipe-grid {
            grid-template-columns: 1fr;
        }
    }
</style>
