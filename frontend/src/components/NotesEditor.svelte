<script>
    import { onMount } from "svelte";
    import {
        recipeStore,
        updateRecipeStore,
        deleteElementStore,
        swapElementsStore,
    } from "../stores/RecipeStore.js";

    export let notes = [];

    let newNote = "";
    let recipeNotes = [];
    let textareaElement;

    onMount(() => {
        if (notes && notes.length > 0) {
            // Initialize with provided notes if available
            recipeNotes = [...notes];
        }

        // Subscribe to store changes
        const unsubscribe = recipeStore.subscribe((recipe) => {
            recipeNotes = recipe.notes || [];
        });

        // Initialize textarea height for any existing content
        setTimeout(() => {
            if (textareaElement && newNote.length > 0) {
                textareaElement.style.height = "45px";
                textareaElement.style.height = textareaElement.scrollHeight + "px";
            }
        }, 0);

        return unsubscribe;
    });

    function addNote() {
        if (newNote.trim()) {
            updateRecipeStore("notes", newNote);
            // Reset the form
            newNote = "";
            // Reset textarea height
            if (textareaElement) {
                textareaElement.style.height = "45px";
            }
        }
    }

    function moveNote(index, direction) {
        const newIndex = index + direction;
        if (newIndex >= 0 && newIndex < recipeNotes.length) {
            swapElementsStore("notes", index, newIndex);
        }
    }

    function removeNote(index) {
        deleteElementStore("notes", index);
    }
    
    // Auto-resize textarea as content grows
    function resizeTextarea(event) {
        const textarea = event.target;
        // Reset height to get accurate scrollHeight
        textarea.style.height = "45px";
        // Set the height to scrollHeight to fit content
        textarea.style.height = textarea.scrollHeight + "px";
    }
</script>

<section class="section-card">
    <h3 class="section-title">Notater</h3>

    <div class="form-row">
        <textarea
            class="textarea-field"
            placeholder="Notat"
            bind:value={newNote}
            bind:this={textareaElement}
            on:input={resizeTextarea}
            rows="1"
        ></textarea>
        <button class="btn" on:click={addNote}>Legg til Notat</button>
    </div>

    <div class="item-list">
        {#each recipeNotes as note, index}
            <div class="list-item">
                <div class="list-bullet">•</div>
                <div class="list-item-content">
                    {note}
                </div>
                <div class="action-buttons">
                    <button
                        class="action-btn"
                        on:click={() => moveNote(index, 1)}
                        aria-label="Move down"
                        disabled={index === recipeNotes.length - 1}
                    >
                        <svg
                            class="action-icon"
                            viewBox="0 0 24 24"
                            stroke="var(--text-on-primary)"
                            stroke-width="2"
                            fill="none"
                        >
                            <polyline points="6 9 12 15 18 9"></polyline>
                        </svg>
                    </button>
                    <button
                        class="action-btn"
                        on:click={() => moveNote(index, -1)}
                        aria-label="Move up"
                        disabled={index === 0}
                    >
                        <svg
                            class="action-icon"
                            viewBox="0 0 24 24"
                            stroke="var(--text-on-primary)"
                            stroke-width="2"
                            fill="none"
                        >
                            <polyline points="18 15 12 9 6 15"></polyline>
                        </svg>
                    </button>
                    <button
                        class="action-btn"
                        on:click={() => removeNote(index)}
                        aria-label="Delete"
                    >
                        <svg
                            class="action-icon"
                            viewBox="0 0 24 24"
                            stroke="var(--text-on-primary)"
                            stroke-width="2"
                            fill="none"
                        >
                            <polyline points="3 6 5 6 21 6"></polyline>
                            <path
                                d="M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2"
                            ></path>
                        </svg>
                    </button>
                </div>
            </div>
        {/each}
    </div>
</section>

<style>
    .section-card {
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

    .form-row {
        display: flex;
        gap: var(--spacing-md);
        margin-bottom: var(--spacing-md);
        align-items: flex-start;
    }

    .textarea-field {
        background-color: var(--input-background);
        border: none;
        border-radius: var(--input-radius);
        padding: 12px 15px;
        font-size: 16px;
        flex-grow: 1;
        min-height: 45px;
        max-height: 200px;
        overflow-y: hidden;
        resize: none;
        font-family: var(--default-font);
        line-height: 1.5;
    }

    .textarea-field::placeholder {
        color: var(--text-light);
    }

    .btn {
        background-color: var(--primary-color);
        color: var(--text-on-primary);
        border: none;
        border-radius: var(--button-radius);
        padding: 12px 15px;
        font-size: 16px;
        cursor: pointer;
        text-align: center;
        height: 45px;
        width: 180px;
        flex-shrink: 0;
    }

    .item-list {
        margin-top: var(--spacing-lg);
    }

    .list-item {
        display: flex;
        align-items: flex-start;
        margin-bottom: var(--spacing-md);
    }

    .list-item-content {
        flex-grow: 1;
        padding-left: var(--spacing-sm);
        padding-right: var(--spacing-sm);
        word-break: break-word;
    }

    .action-buttons {
        display: flex;
        gap: 5px;
    }

    .action-btn {
        width: 40px;
        height: 40px;
        border-radius: 5px;
        border: none;
        background-color: var(--primary-color);
        color: var(--text-on-primary);
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
    }

    .action-btn:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }

    .list-bullet {
        min-width: 20px;
        padding-top: 2px;
    }

    /* On smaller screens, make the button take full width on its own row */
    @media (max-width: 640px) {
        .form-row {
            flex-direction: column;
            gap: var(--spacing-md);
        }

        .textarea-field {
            width: 100%;
        }

        .btn {
            width: 100%;
            margin-top: 5px;
        }
    }
</style>