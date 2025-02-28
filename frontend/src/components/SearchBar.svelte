<!-- SearchBar.svelte -->
<script>
    import { createEventDispatcher } from "svelte";
    import { searchRecipeApi } from "./APIFunctions.js";

    const dispatch = createEventDispatcher();

    const optionsMap = {
        category: ["Middag", "Dessert", "Suppe", "Forett", "Bakst", "Kake"],
        region: ["Asia", "Italia", "Frankrike", "Norge", "Annet"],
    };

    const keys = ["Ingredienser", ...Object.keys(optionsMap)];

    let selectedKey = keys[0];
    let selectedValue = "";
    let searchQueryString = "";

    // Create URL-friendly search string
    $: {
        // Format search query depending on the backend requirements
        if (selectedValue) {
            searchQueryString = encodeURIComponent(
                JSON.stringify({ [selectedKey]: selectedValue }),
            );
        } else {
            searchQueryString = "";
        }
    }

    async function handleSubmit(event) {
        event.preventDefault();

        if (!selectedValue) {
            // If no value, show all recipes
            dispatch("search", { results: [] });
            return;
        }

        try {
            const results = await searchRecipeApi(searchQueryString);
            dispatch("search", { results });
        } catch (error) {
            console.error("Search error:", error);
            dispatch("search", { results: [] });
        }
    }
</script>

<form class="search-bar" on:submit={handleSubmit}>
    <div class="dropdown-container">
        <select class="search-dropdown" bind:value={selectedKey}>
            {#each keys as key}
                <option value={key}>{key}</option>
            {/each}
        </select>
        <svg
            class="dropdown-arrow"
            width="12"
            height="6"
            viewBox="0 0 12 6"
            fill="none"
        >
            <path d="M1 1L6 5L11 1" stroke="black" stroke-width="1.5" />
        </svg>
    </div>

    {#if selectedKey === "Ingredienser"}
        <input
            class="search-input"
            type="search"
            placeholder="Type ingredients..."
            bind:value={selectedValue}
        />
    {:else if optionsMap[selectedKey]}
        <div class="value-dropdown-container">
            <select class="value-dropdown" bind:value={selectedValue}>
                <option value="">Select {selectedKey}</option>
                {#each optionsMap[selectedKey] as value}
                    <option {value}>{value}</option>
                {/each}
            </select>
        </div>
    {/if}

    <button type="submit" class="search-button" aria-label="Search">
        <svg
            viewBox="0 0 24 24"
            width="28"
            height="28"
            stroke="currentColor"
            stroke-width="2"
            fill="none"
        >
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
        </svg>
    </button>
</form>

<style>
    .search-bar {
        background: #d9d9d9;
        border-radius: 24px;
        display: flex;
        align-items: center;
        padding: 0 10px 0 20px;
        margin-bottom: 40px;
        height: 68px;
        position: relative;
    }

    .search-dropdown,
    .value-dropdown {
        background: transparent;
        border: none;
        font-size: 22px;
        color: rgba(0, 0, 0, 0.7);
        cursor: pointer;
        outline: none;
        appearance: none;
        height: 100%;
    }

    .search-dropdown {
        width: 140px;
        padding-right: 15px;
    }

    .value-dropdown {
        width: 100%;
    }

    .dropdown-container,
    .value-dropdown-container {
        position: relative;
        display: flex;
        align-items: center;
    }

    .dropdown-container {
        margin-right: 15px;
        border-right: 1px solid rgba(0, 0, 0, 0.2);
    }

    .value-dropdown-container {
        flex-grow: 1;
    }

    .dropdown-arrow {
        position: absolute;
        right: 15px;
        top: 50%;
        transform: translateY(-50%);
        pointer-events: none;
    }

    .search-input {
        background: transparent;
        border: none;
        font-size: 32px;
        color: rgba(0, 0, 0, 0.5);
        width: 100%;
        outline: none;
    }

    .search-button {
        background: transparent;
        border: none;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0 10px;
        transition: transform 0.2s;
        min-width: 48px;
    }

    .search-button:hover {
        transform: scale(1.1);
    }
</style>
