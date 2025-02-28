<!-- SearchResults.svelte -->
<script>
    import RecipeCard from "./RecipeCard.svelte";

    export let recipes = [];
    let displayedRecipes = recipes;
    let searchPerformed = false;

    export function updateResults(results) {
        displayedRecipes = results;
        searchPerformed = true;
    }

    export function resetResults() {
        displayedRecipes = recipes;
        searchPerformed = false;
    }
</script>

<div class="recipe-grid">
    {#if displayedRecipes && displayedRecipes.length > 0}
        {#each displayedRecipes as recipe (recipe._id)}
            <RecipeCard {recipe} />
        {/each}
    {:else if searchPerformed}
        <div class="no-results">
            <p>No recipes found. Try a different search.</p>
        </div>
    {:else}
        <div class="no-results">
            <p>No recipes available.</p>
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
