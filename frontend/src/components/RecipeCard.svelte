<script>
    import { onMount } from "svelte";
    
    export let recipe = {};
    let isLargeScreen = false;

    onMount(() => {
        // Check screen size and listen for changes
        checkScreenSize();
        window.addEventListener('resize', checkScreenSize);
        
        return () => {
            window.removeEventListener('resize', checkScreenSize);
        };
    });

    function checkScreenSize() {
        isLargeScreen = window.innerWidth >= 768;
    }
    
    // Truncate long titles
    function truncateText(text, maxLength = 24) {
        if (!text) return '';
        return text.length > maxLength 
            ? text.substring(0, maxLength) + '...' 
            : text;
    }
</script>

<a href={`/recipe/${recipe._id}`} class="card-link-wrapper">
    <article class="recipe-card">
        <div class="card-header">
            <h2 class="card-title">{truncateText(recipe.recipeName || "Uten navn", isLargeScreen ? 30 : 24)}</h2>
            {#if recipe.favorite}
                <span class="favorite-indicator">
                    <svg
                        viewBox="0 0 24 24"
                        stroke="var(--accent-color)"
                        stroke-width="2"
                        fill="var(--accent-color)"
                        class="favorite-icon"
                    >
                        <path
                            d="M12 2L15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2z"
                        ></path>
                    </svg>
                </span>
            {/if}
        </div>
        
        {#if recipe.time}
            <div class="card-footer">
                <div class="time-display">
                    <svg class="clock-icon" viewBox="0 0 24 24" stroke="var(--text-on-primary)" stroke-width="2" fill="none">
                        <circle cx="12" cy="12" r="10"></circle>
                        <polyline points="12 6 12 12 16 14"></polyline>
                    </svg>
                    <span>{recipe.time}</span>
                </div>
            </div>
        {/if}
    </article>
</a>

<style>
    .card-link-wrapper {
        text-decoration: none;
        color: inherit;
        display: block;
        height: 100%;
    }

    .recipe-card {
        background-color: var(--primary-color);
        border-radius: var(--card-radius);
        padding: var(--spacing-lg);
        color: var(--text-on-primary);
        box-shadow: var(--card-shadow);
        display: flex;
        flex-direction: column;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        height: 100%;
    }

    .recipe-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--floating-button-shadow);
    }

    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: var(--spacing-md);
    }

    .card-title {
        font-size: 24px;
        font-weight: 700;
        margin: 0;
        color: var(--text-on-primary);
    }

    .favorite-indicator {
        display: flex;
        align-items: center;
    }

    .favorite-icon {
        width: 24px;
        height: 24px;
    }

    .card-footer {
        margin-top: auto;
    }

    .time-display {
        display: flex;
        align-items: center;
        gap: var(--spacing-sm);
        font-size: 16px;
    }

    .clock-icon {
        width: 18px;
        height: 18px;
    }

    /* Large screen enhancements */
    @media (min-width: 768px) {
        .card-title {
            font-size: 20px;
        }
    }
    
    /* Small screen adjustments */
    @media (max-width: 767px) {
        .recipe-card {
            padding: var(--spacing-md);
        }
        
        .time-display {
            font-size: 14px;
        }
    }
</style>