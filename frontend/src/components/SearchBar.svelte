<script>
    import { searchRecipeApi } from "./APIFunctions.js";
    import { searchResults, hasSearched } from "../stores/SearchStore.js";
    import { onMount } from "svelte";

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
            "Tilbehør"
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
        ]
    };

    const keys = ["Favorite", "Oppskrift", "Ingredienser", "Opphav", ...Object.keys(optionsMap)];

    let selectedKey = "Favorite"; // Default to Favorite
    let selectedValue = "Alle"; // Default to show all
    let searchQueryString = "";
    let noRecipesFound = false;
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

    // Create URL-friendly search string
    $: {
        if (selectedKey === "Favorite" && selectedValue === "Ja") {
            searchQueryString = JSON.stringify({
                "favorite": true
            });
        } else if (selectedKey === "Ingredienser" && selectedValue) {
            // Handle comma-separated ingredients
            const ingredients = selectedValue.split(",").map(ing => ing.trim()).filter(ing => ing);
            searchQueryString = JSON.stringify({
                "ingredients": ingredients,
                "partial": true,
                "caseInsensitive": true
            });
        } else if (selectedKey === "Oppskrift" && selectedValue) {
            searchQueryString = JSON.stringify({
                "recipeName": selectedValue,
                "partial": true,
                "caseInsensitive": true
            });
        } else if (selectedKey === "Opphav" && selectedValue) {
            searchQueryString = JSON.stringify({
                "origin": selectedValue,
                "partial": true,
                "caseInsensitive": true
            });
        } else if (optionsMap[selectedKey] && selectedValue) {
            searchQueryString = JSON.stringify({
                [selectedKey]: selectedValue
            });
        } else {
            searchQueryString = "";
        }
    }

    async function handleSubmit(event) {
        event.preventDefault();

        // If Favorite is selected and value is "Alle" or no value for other options, show all recipes
        if ((selectedKey === "Favorite" && selectedValue === "Alle") || 
            (selectedKey !== "Favorite" && !selectedValue)) {
            searchResults.set([]);
            hasSearched.set(false);
            noRecipesFound = false;
            return;
        }

        try {
            const results = await searchRecipeApi(searchQueryString);
            noRecipesFound = results.length === 0;
            searchResults.set(results);
            hasSearched.set(true);
        } catch (error) {
            console.error("Search error:", error);
            searchResults.set([]);
            hasSearched.set(true);
            noRecipesFound = true;
        }
    }

    // Handle key change
    $: {
        if (selectedKey === "Favorite") {
            selectedValue = "Alle"; // Default to "Alle" when Favorite is selected
        } else {
            selectedValue = ""; // Reset value for other options
        }
    }
</script>

<form class="search-bar" on:submit={handleSubmit}>
    <div class="search-controls">
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
                placeholder="Skill ingredienser med komma..."
                bind:value={selectedValue}
            />
        {:else if selectedKey === "Oppskrift"}
            <input
                class="search-input"
                type="search"
                placeholder="Søk etter navnet på oppskriften..."
                bind:value={selectedValue}
            />
        {:else if selectedKey === "Opphav"}
            <input
                class="search-input"
                type="search"
                placeholder="Søk etter opphav..."
                bind:value={selectedValue}
            />
        {:else if selectedKey === "Favorite"}
            <div class="value-dropdown-container">
                <select class="value-dropdown" bind:value={selectedValue}>
                    <option value="Alle">Alle</option>
                    <option value="Ja">Ja</option>
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
    </div>

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

{#if noRecipesFound}
    <div class="no-results-banner">
        <p>Ingen oppskrifter funnet</p>
    </div>
{/if}

<style>
    .search-bar {
        background: var(--input-background);
        border-radius: var(--card-radius);
        display: flex;
        flex-direction: column;
        align-items: stretch;
        padding: var(--spacing-md);
        margin-bottom: 40px;
        gap: var(--spacing-md);
    }

    .search-controls {
        display: flex;
        flex-direction: column;
        gap: var(--spacing-md);
    }

    .dropdown-container,
    .value-dropdown-container {
        position: relative;
        display: flex;
        align-items: center;
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
        width: 100%;
        padding-right: 24px;
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
        background-color: var(--primary-color);
        border: none;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 12px;
        border-radius: var(--button-radius);
        transition: transform 0.2s;
    }

    .search-button:hover {
        transform: scale(1.05);
        background-color: var(--primary-color-dark);
    }
    
    .search-button svg {
        stroke: var(--text-on-primary);
    }

    .no-results-banner {
        background: var(--card-background);
        color: var(--primary-color);
        padding: var(--spacing-md);
        border-radius: var(--card-radius);
        text-align: center;
        margin-bottom: 20px;
        font-size: 18px;
        font-weight: 500;
        box-shadow: var(--card-shadow);
    }

    /* Responsive adjustments for large screens */
    @media (min-width: 768px) {
        .search-bar {
            flex-direction: row;
            align-items: center;
            padding: 0 var(--spacing-sm) 0 var(--spacing-lg);
            height: 68px;
        }

        .search-controls {
            flex-direction: row;
            flex-grow: 1;
            gap: 0;
        }

        .dropdown-container {
            width: 160px;
            border-right: 1px solid rgba(0, 0, 0, 0.2);
            margin-right: 15px;
        }

        .value-dropdown-container {
            flex-grow: 1;
        }

        .search-button {
            min-width: 48px;
            height: 48px;
            border-radius: 0;
            background: transparent;
        }
        
        .search-button svg {
            stroke: var(--icon-color);
        }
    }
</style>