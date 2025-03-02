<script>
    export let notes = [];

    // Computed property to check if notes exist and are not empty
    $: hasNotes = notes && notes.length > 0;
</script>

{#if hasNotes}
<section class="recipe-section">
    <h3 class="section-title">Notater</h3>
    <div class="notes-content">
        <ul class="notes-list">
            {#each notes as note}
                <li class="note-item">
                    <span class="note-bullet">•</span>
                    <span class="note-text">{note}</span>
                </li>
            {/each}
        </ul>
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

    .notes-content {
        color: var(--text-dark);
        font-size: 16px;
        line-height: 1.6;
    }

    .notes-list {
        list-style: none;
        padding: 0;
        margin: 0;
    }

    .note-item {
        display: flex;
        margin-bottom: 10px;
        align-items: flex-start;
    }

    .note-bullet {
        margin-right: 10px;
        color: var(--primary-color, #55a7ac);
    }

    .note-text {
        flex: 1;
    }
</style>