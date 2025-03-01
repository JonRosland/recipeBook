<script>
    export let ingredients = [];
    export let defaultPortion = 1;

    // Ensure defaultPortion is an integer
    let basePortionSize = parseInt(defaultPortion) || 1;
    // Initialize current portion to the default
    let currentPortion = basePortionSize;

    function decreasePortion() {
        if (currentPortion > 1) {
            currentPortion -= 1;
        }
    }

    function increasePortion() {
        currentPortion += 1;
    }

    /**
     * Calculate scaled quantity based on portion size
     * @param {number} baseQuantity - Original quantity from recipe
     * @returns {string} - Formatted scaled quantity
     */

    function calculateQuantity(baseQuantity) {
        // Handle empty or invalid values
        if (
            baseQuantity === null ||
            baseQuantity === undefined ||
            isNaN(baseQuantity)
        ) {
            return "";
        }

        // Cast to number and ensure valid values
        const quantity = Number(baseQuantity);
        const basePortion = Number(basePortionSize) || 1;
        const currentPortionNum = Number(currentPortion) || 1;

        // Calculate scaled quantity
        const scaleFactor = currentPortionNum / basePortion;
        const scaledQuantity = quantity * scaleFactor;

        // Format the result (show decimals only when needed)
        return Number.isInteger(scaledQuantity)
            ? scaledQuantity.toString()
            : scaledQuantity.toFixed(1);
    }
</script>

<section class="recipe-section ingredients-section">
    <div class="section-header">
        <h3 class="section-title">Ingredienser</h3>
        <div class="quantity-control">
            <button
                class="qty-button"
                on:click={decreasePortion}
                aria-label="Decrease quantity">−</button
            >
            <input
                type="number"
                class="qty-input"
                bind:value={currentPortion}
                aria-label="Quantity"
                min="1"
            />
            <button
                class="qty-button"
                on:click={increasePortion}
                aria-label="Increase quantity">+</button
            >
        </div>
    </div>
    <div class="ingredient-list">
        {#if ingredients && ingredients.length > 0}
            {#each ingredients as ingredient}
                <div class="ingredient">
                    <span class="ingredient-name">{ingredient.name || ""}:</span
                    >
                    <span class="ingredient-quantity"
                        >{calculateQuantity(ingredient.quantity)}</span
                    >
                    <span class="ingredient-unit">{ingredient.unit || ""}</span>
                </div>
            {/each}
        {:else}
            <div class="no-ingredients">Ingen ingredienser registrert.</div>
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
        font-weight: 500;
    }

    .ingredient-list {
        margin-top: var(--spacing-lg);
    }

    .ingredient {
        font-size: 18px;
        margin-bottom: 12px;
        display: flex;
        align-items: baseline;
        flex-wrap: wrap;
        gap: 4px;
    }

    .ingredient-name {
        font-weight: 500;
    }

    .ingredient-quantity {
        font-weight: bold;
    }

    .ingredient-unit {
        margin-left: 2px;
    }

    .section-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: var(--spacing-lg);
    }

    .quantity-control {
        display: flex;
        align-items: center;
        background-color: var(--card-background);
        border-radius: 30px;
        overflow: hidden;
        width: 120px;
        height: 40px;
        box-shadow: var(--button-shadow);
    }

    .qty-button {
        background-color: var(--primary-color);
        color: var(--text-on-primary);
        border: none;
        width: 40px;
        height: 40px;
        font-size: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        flex-shrink: 0;
    }

    .qty-input {
        width: 40px;
        height: 40px;
        text-align: center;
        font-size: 20px;
        border: none;
        background: var(--card-background);
        flex-grow: 1;
        font-weight: 500;
        -moz-appearance: textfield; /* Firefox */
    }

    /* Hide spinner for other browsers */
    .qty-input::-webkit-outer-spin-button,
    .qty-input::-webkit-inner-spin-button {
        -webkit-appearance: none;
        margin: 0;
    }

    .no-ingredients {
        font-style: italic;
        color: var(--text-light);
    }
</style>
