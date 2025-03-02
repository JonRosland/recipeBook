<script>
    import { onMount } from "svelte";
    import RecipeCard from "./RecipeCard.svelte";
    import { searchResults, hasSearched } from "../stores/SearchStore.js";

    export let recipes = [];
    let displayedRecipes = [];
    let isLargeScreen = false;
    let selectedCategory = "All";

    // Categories for filtering on larger screens
    const categories = [
        "All",
        "Middag",
        "Dessert",
        "Suppe",
        "Forett",
        "Søt bakst",
        "Grov bakst",
        "Kake",
        "Lunsj",
        "Salat",
        "Pasta",
        "Pizza",
        "Sauser",
        "Snacks",
        "Grillmat",
        "Sjømat",
        "Småretter",
        "Streetfood",
        "Tilbehør"
    ];

    onMount(() => {
        // Initialize with all recipes
        displayedRecipes = recipes;

        // Check screen size and listen for changes
        checkScreenSize();
        window.addEventListener('resize', checkScreenSize);

        // Subscribe to search results
        const unsubscribe = searchResults.subscribe((results) => {
            if (results.length > 0) {
                displayedRecipes = results;
            } else {
                displayedRecipes = recipes;
            }
        });

        return () => {
            window.removeEventListener('resize', checkScreenSize);
            unsubscribe();
        };
    });

    function checkScreenSize() {
        isLargeScreen = window.innerWidth >= 768;
    }

    // Filter by category (only on large screens)
    $: filteredRecipes = (isLargeScreen && selectedCategory !== 'All') 
        ? displayedRecipes.filter(recipe => recipe.category === selectedCategory)
        : displayedRecipes;
</script>

<!-- Optional category filters for large screens -->
{#if isLargeScreen}
    <div class="category-filters">
        {#each categories as category}
            <button 
                class="category-filter {selectedCategory === category ? 'active' : ''}" 
                on:click={() => selectedCategory = category}
            >
                {category}
            </button>
        {/each}
    </div>
{/if}

<!-- Recipe grid with responsive columns -->
<div class="recipe-grid {isLargeScreen ? 'large-grid' : ''}">
    {#if filteredRecipes && filteredRecipes.length > 0}
        {#each filteredRecipes as recipe (recipe._id)}
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
        grid-template-columns: repeat(2, 1fr);
        gap: 20px;
        margin-bottom: 100px;
    }

    .large-grid {
        gap: 30px;
    }

    .no-results {
        grid-column: 1 / -1;
        text-align: center;
        padding: 40px;
        color: var(--primary-color, #55a7ac);
        font-size: 24px;
        background-color: var(--card-background);
        border-radius: var(--card-radius);
        box-shadow: var(--card-shadow);
    }

    .category-filters {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-bottom: 30px;
    }

    .category-filter {
        padding: 8px 16px;
        background-color: var(--card-background);
        border: 1px solid var(--primary-color-light);
        border-radius: 20px;
        color: var(--text-dark);
        cursor: pointer;
        transition: all 0.2s ease;
        font-size: 14px;
    }

    .category-filter:hover {
        background-color: var(--primary-color-light);
        color: var(--text-on-primary);
    }

    .category-filter.active {
        background-color: var(--primary-color);
        color: var(--text-on-primary);
        border-color: var(--primary-color);
    }

    /* Responsive adjustments */
    @media (min-width: 768px) {
        .recipe-grid {
            grid-template-columns: repeat(3, 1fr);
        }
    }

    @media (min-width: 1024px) {
        .recipe-grid {
            grid-template-columns: repeat(4, 1fr);
        }
    }
</style>