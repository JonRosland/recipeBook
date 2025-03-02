<script>
    import { toggleFavoriteApi } from "./APIFunctions.js";
    import { onMount } from "svelte";

    export let title = "";
    export let origin = "";
    export let recipeId = "";
    export let favorite = false;
    export let isDesktopView = false;

    // Local reactive state
    let isFavorite = false;

    onMount(() => {
        // Initialize the local state when the component mounts
        isFavorite = favorite;
        
        // Check if we're on desktop
        checkDesktopView();
        window.addEventListener('resize', checkDesktopView);
        
        return () => {
            window.removeEventListener('resize', checkDesktopView);
        };
    });
    
    function checkDesktopView() {
        isDesktopView = window.innerWidth >= 1024;
    }

    // Update when the prop changes
    $: isFavorite = favorite;

    async function toggleFavorite() {
        try {
            await toggleFavoriteApi(recipeId, !isFavorite);
            isFavorite = !isFavorite;
        } catch (error) {
            console.error("Error toggling favorite status:", error);
        }
    }
    
    // Expose method to update desktop state from outside
    export function updateDesktopState(isDesktop) {
        isDesktopView = isDesktop;
    }
</script>

<header class="recipe-header">
    <a href="/" class="back-button" aria-label="Go back">
        <svg
            class="back-icon"
            viewBox="0 0 24 24"
            stroke="var(--icon-color)"
            stroke-width="2"
            fill="none"
        >
            <path d="M15 6l-6 6 6 6"></path>
        </svg>
    </a>
    <div class="header-content">
        <h1 class="recipe-title">{title}</h1>
        
        <!-- Only show origin in header on mobile view -->
        {#if origin && !isDesktopView}
            <h2 class="recipe-origin header-origin">Opphav: {origin}</h2>
        {/if}
    </div>
    <div class="header-actions">
        <button
            class="favorite-button"
            on:click={toggleFavorite}
            aria-label={isFavorite
                ? "Remove from favorites"
                : "Add to favorites"}
        >
            <svg
                class="favorite-icon"
                viewBox="0 0 24 24"
                stroke="var(--accent-color)"
                stroke-width="2"
                fill={isFavorite ? "var(--accent-color)" : "none"}
            >
                <path
                    d="M12 2L15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2z"
                ></path>
            </svg>
        </button>
        <a
            href={`/edit/${recipeId}`}
            class="edit-button"
            aria-label="Edit recipe"
        >
            <svg
                class="edit-icon"
                viewBox="0 0 24 24"
                stroke="var(--icon-color)"
                stroke-width="2"
                fill="none"
            >
                <path
                    d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"
                ></path>
            </svg>
        </a>
    </div>
</header>

<style>
    .recipe-header {
        text-align: center;
        position: relative;
        margin-bottom: var(--spacing-xxl);
        padding: var(--spacing-sm) 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .header-content {
        flex-grow: 1;
        padding: 0 var(--spacing-sm);
    }

    .recipe-title {
        color: var(--primary-color);
        font-size: 32px;
        font-weight: 500;
        margin-bottom: var(--spacing-sm);
    }

    .recipe-origin {
        font-size: 18px;
        color: var(--text-dark);
        font-weight: 400;
    }

    .header-actions {
        display: flex;
        gap: 8px;
    }

    .back-button,
    .edit-button,
    .favorite-button {
        background: none;
        border: none;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 40px;
        height: 40px;
        text-decoration: none;
    }

    .back-icon,
    .edit-icon {
        width: 24px;
        height: 24px;
        stroke: var(--icon-color);
        stroke-width: 2;
        fill: none;
    }

    .favorite-icon {
        width: 24px;
        height: 24px;
        stroke: var(--accent-color);
        stroke-width: 2;
    }

    @media (max-width: 480px) {
        .recipe-title {
            font-size: 28px;
        }

        .recipe-origin {
            font-size: 16px;
        }
    }
</style>