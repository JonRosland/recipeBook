<!-- RecipeCard.svelte -->
<script>
    import { toggleFavoriteApi } from "./APIFunctions.js";

    export let recipe = {};

    const toggleFavorite = async (e) => {
        e.preventDefault();
        try {
            await toggleFavoriteApi(recipe._id, !recipe.favorite);
            recipe.favorite = !recipe.favorite;
        } catch (error) {
            console.error("Error updating favorite status:", error);
        }
    };
</script>

<article class="recipe-card">
    <div class="card-header">
        <h2 class="card-title">{recipe.recipeName}</h2>
        <button
            class="favorite-btn"
            on:click={toggleFavorite}
            aria-label={recipe.favorite
                ? "Remove from favorites"
                : "Add to favorites"}
        >
            <svg
                viewBox="0 0 24 24"
                stroke="currentColor"
                stroke-width="2"
                fill={recipe.favorite ? "currentColor" : "none"}
            >
                <path
                    d="M12 2L15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2z"
                ></path>
            </svg>
        </button>
    </div>
    <a href={`/recipe/${recipe._id}`} class="card-link">
        <div class="card-footer">
            <p class="category">{recipe.category || ""}</p>
            <p class="duration">{recipe.time || 0} min</p>
        </div>
    </a>
</article>

<style>
    .recipe-card {
        background-color: var(--primary-color, #55a7ac);
        border-radius: 24px;
        padding: 20px;
        color: #ffffff;
        box-shadow: 0 4px 4px rgba(0, 0, 0, 0.25);
        display: flex;
        flex-direction: column;
        transition: transform 0.2s ease;
        height: 100%;
    }

    .recipe-card:hover {
        transform: translateY(-4px);
    }

    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 20px;
    }

    .card-title {
        font-size: 32px;
        font-weight: 700;
        margin: 0;
    }

    .favorite-btn {
        background: none;
        border: none;
        cursor: pointer;
        padding: 0;
        color: #ffffff;
    }

    .favorite-btn svg {
        width: 48px;
        height: 48px;
    }

    .card-link {
        text-decoration: none;
        color: inherit;
        display: flex;
        flex-direction: column;
        flex-grow: 1;
    }

    .card-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: auto;
    }

    .category {
        font-size: 32px;
        font-weight: 400;
        margin: 0;
    }

    .duration {
        font-size: 20px;
        text-align: center;
        margin: 0;
    }
</style>
