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

<a href={`/recipe/${recipe._id}`} class="card-link-wrapper">
    <article class="recipe-card">
        <div class="card-header">
            <h2 class="card-title">{recipe.recipeName || "Uten navn"}</h2>
            <button
                class="favorite-btn"
                on:click={(e) => {
                    e.preventDefault();
                    toggleFavorite(e);
                }}
                aria-label={recipe.favorite
                    ? "Remove from favorites"
                    : "Add to favorites"}
            >
                <svg
                    viewBox="0 0 24 24"
                    stroke="var(--accent-color)"
                    stroke-width="2"
                    fill={recipe.favorite ? "var(--accent-color)" : "none"}
                    class="favorite-icon"
                >
                    <path
                        d="M12 2L15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2z"
                    ></path>
                </svg>
            </button>
        </div>
        <div class="card-footer">
            <p class="category">{recipe.category || ""}</p>
            <p class="duration">
                <svg
                    class="clock-icon"
                    viewBox="0 0 24 24"
                    stroke="var(--text-on-primary)"
                    stroke-width="2"
                    fill="none"
                >
                    <circle cx="12" cy="12" r="10"></circle>
                    <polyline points="12 6 12 12 16 14"></polyline>
                </svg>
                {recipe.time || ""}
            </p>
        </div>
    </article>
</a>

<style>
    .recipe-card {
        background-color: var(--primary-color);
        border-radius: var(--card-radius);
        padding: var(--spacing-lg);
        color: var(--text-on-primary);
        box-shadow: var(--card-shadow);
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
        font-size: 24px;
        font-weight: 700;
        margin: 0;
        color: var(--text-on-primary);
    }

    .favorite-btn {
        background: none;
        border: none;
        cursor: pointer;
        padding: 0;
        color: #ffffff;
    }

    .favorite-btn svg {
        width: 24px;
        height: 24px;
    }

    .card-link-wrapper {
        text-decoration: none;
        color: inherit;
        display: block;
        height: 100%;
    }

    .card-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: auto;
    }

    .category {
        font-size: 18px;
        font-weight: 400;
        margin: 0;
    }

    .duration {
        font-size: 14px;
        text-align: center;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 4px;
    }

    .clock-icon {
        width: 16px;
        height: 16px;
    }
</style>
