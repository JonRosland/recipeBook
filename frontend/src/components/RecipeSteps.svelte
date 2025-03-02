<script>
    export let steps = [];
    
    // Check if steps exist and are not empty
    $: hasSteps = steps && steps.length > 0;
</script>

{#if hasSteps}
<section class="recipe-section">
    <h3 class="section-title">Fremgangsmåte</h3>
    <div class="steps-content">
        <ol class="steps-list">
            {#each steps as step, index}
                <li class="step-item">
                    <span class="step-number">{index + 1}.</span>
                    <span class="step-text">{step}</span>
                </li>
            {/each}
        </ol>
    </div>
</section>
{/if}

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

    .steps-content {
        color: var(--text-dark);
        font-size: 16px;
        line-height: 1.6;
    }

    .steps-list {
        list-style: none;
        padding: 0;
        margin: 0;
    }

    .step-item {
        display: flex;
        margin-bottom: 15px;
        align-items: flex-start;
    }

    .step-number {
        font-weight: bold;
        margin-right: 10px;
        color: var(--primary-color, #55a7ac);
        min-width: 25px;
    }

    .step-text {
        flex: 1;
    }
</style>