<script>
    import { searchRecipeApi } from "./APIFunctions.js";
    import { searchResults, hasSearched } from "../stores/SearchStore.js";

    const optionsMap = {
        category: [
            "Middag",
            "Dessert",
            "Suppe",
            "Forett",
            "Søt bakst",
            "Grov bakst",
            "Kake",
            "Lunsj",
            "Salat",
            "Pasta",
            "Pizza",
            "Sauser",
            "Snacks",
            "Grillmat",
            "Sjømat",
            "Småretter",
            "Streetfood",
        ],
        region: [
            "Asia",
            "Italia",
            "Frankrike",
            "Nordisk",
            "India",
            "Middelhavet",
            "Slavisk",
            "Meksikansk",
            "Europa",
            "Ukategorisert",
        ],
    };

    const keys = ["Ingredienser", ...Object.keys(optionsMap)];

    let selectedKey = keys[0];
    let selectedValue = "";
    let searchQueryString = "";

    // Create URL-friendly search string
    $: {
        if (selectedValue) {
            searchQueryString = JSON.stringify({
                [selectedKey]: selectedValue,
            });
        } else {
            searchQueryString = "";
        }
    }

    async function handleSubmit(event) {
        event.preventDefault();

        if (!selectedValue) {
            // Reset to show all recipes
            searchResults.set([]);
            hasSearched.set(false);
            return;
        }

        try {
            const results = await searchRecipeApi(searchQueryString);
            searchResults.set(results);
            hasSearched.set(true);
        } catch (error) {
            console.error("Search error:", error);
            searchResults.set([]);
            hasSearched.set(true);
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
            stroke="var(--icon-color)"
            stroke-width="1.5"
        >
            <path d="M1 1L6 5L11 1"></path>
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
                <option value="">Velg {selectedKey}</option>
                {#each optionsMap[selectedKey] as value}
                    <option value={value}>{value}</option>
                {/each}
            </select>
            <svg
                class="dropdown-arrow"
                width="12"
                height="6"
                viewBox="0 0 12 6"
                fill="none"
                stroke="var(--icon-color)"
                stroke-width="1.5"
            >
                <path d="M1 1L6 5L11 1"></path>
            </svg>
        </div>
    {/if}

    <button type="submit" class="search-button" aria-label="Search">
        <svg
            viewBox="0 0 24 24"
            width="28"
            height="28"
            stroke="var(--icon-color)"
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
        background: var(--input-background);
        border-radius: var(--card-radius);
        display: flex;
        align-items: center;
        padding: 0 var(--spacing-sm) 0 var(--spacing-lg);
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
        width: 160px;
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
        font-size: 22px;
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
