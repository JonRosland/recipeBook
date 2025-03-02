<script>
    export let recipe = {};
</script>

<section class="recipe-section info-section">
    <h3 class="section-title">Informasjon</h3>
    
    <div class="info-content">
        {#if recipe.origin}
            <div class="info-item">
                <div class="info-icon-container">
                    <svg class="info-icon" viewBox="0 0 24 24" stroke="var(--primary-color)" stroke-width="2" fill="none">
                        <circle cx="12" cy="12" r="10"></circle>
                        <line x1="2" y1="12" x2="22" y2="12"></line>
                        <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
                    </svg>
                </div>
                <span class="info-label">Opphav:</span>
                <span class="info-value">{recipe.origin}</span>
            </div>
        {/if}
        
        {#if recipe.time}
            <div class="info-item">
                <div class="info-icon-container">
                    <svg class="info-icon" viewBox="0 0 24 24" stroke="var(--primary-color)" stroke-width="2" fill="none">
                        <circle cx="12" cy="12" r="10"></circle>
                        <polyline points="12 6 12 12 16 14"></polyline>
                    </svg>
                </div>
                <span class="info-label">Tid:</span>
                <span class="info-value">{recipe.time}</span>
            </div>
        {/if}
        
        {#if recipe.region}
            <div class="info-item">
                <div class="info-icon-container">
                    <svg class="info-icon" viewBox="0 0 24 24" stroke="var(--primary-color)" stroke-width="2" fill="none">
                        <polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"></polygon>
                        <line x1="8" y1="2" x2="8" y2="18"></line>
                        <line x1="16" y1="6" x2="16" y2="22"></line>
                    </svg>
                </div>
                <span class="info-label">Region:</span>
                <span class="info-value">{recipe.region}</span>
            </div>
        {/if}
        
        {#if recipe.category}
            <div class="info-item">
                <div class="info-icon-container">
                    <svg class="info-icon" viewBox="0 0 24 24" stroke="var(--primary-color)" stroke-width="2" fill="none">
                        <path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"></path>
                        <line x1="7" y1="7" x2="7.01" y2="7"></line>
                    </svg>
                </div>
                <span class="info-label">Kategori:</span>
                <span class="info-value">{recipe.category}</span>
            </div>
        {/if}

        {#if recipe.portion}
            <div class="info-item">
                <div class="info-icon-container">
                    <svg class="info-icon" viewBox="0 0 24 24" stroke="var(--primary-color)" stroke-width="2" fill="none">
                        <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                        <circle cx="9" cy="7" r="4"></circle>
                        <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                        <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                    </svg>
                </div>
                <span class="info-label">Porsjoner:</span>
                <span class="info-value">{recipe.portion}</span>
            </div>
        {/if}
    </div>
</section>

<style>
    .recipe-section {
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
    
    .info-content {
        display: flex;
        flex-direction: column;
        gap: var(--spacing-md);
    }
    
    .info-item {
        display: flex;
        flex-direction: row;
        gap: var(--spacing-sm);
        align-items: center;
    }
    
    .info-icon-container {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 24px;
        height: 24px;
    }
    
    .info-icon {
        width: 20px;
        height: 20px;
        stroke: var(--primary-color);
    }
    
    .info-label {
        font-weight: 500;
        color: var(--text-light);
        font-size: 16px;
        min-width: 80px;
    }
    
    .info-value {
        font-size: 18px;
        color: var(--text-dark);
    }
    
    @media (max-width: 767px) {
        .recipe-section {
            padding: var(--spacing-md); /* Reduce padding on small screens */
            margin-bottom: var(--spacing-lg); /* Reduce margin */
        }
        
        .section-title {
            font-size: 22px; /* Smaller title on mobile */
            margin-bottom: var(--spacing-md);
        }
        
        .info-content {
            gap: var(--spacing-sm); /* Tighter spacing */
        }
        
        .info-item {
            display: grid;
            grid-template-columns: auto auto 1fr;
            gap: var(--spacing-sm);
            align-items: center;
        }
        
        .info-label {
            font-size: 14px;
            min-width: unset;
        }
        
        .info-value {
            font-size: 16px;
        }
    }
</style>