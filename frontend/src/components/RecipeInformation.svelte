<script>
    import { onMount } from "svelte";
    import { recipeStore, updateRecipeStore } from "../stores/RecipeStore.js";

    export let recipeData = null;

    // Default values
    let recipeName = "";
    let origin = "";
    let portion = "";
    let category = "";
    let region = "";
    let time = "";

    // Category and region options
    const categories = [
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
        "Tilbehør",
    ];
    const regions = [
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
    ];

    onMount(() => {
        if (recipeData) {
            // If editing existing recipe
            recipeName = recipeData.recipeName || "";
            origin = recipeData.origin || "";
            portion = recipeData.portion ? recipeData.portion.toString() : "";
            category = recipeData.category || "Velg kategori";
            region = recipeData.region || "Velg region";
            // Ensure time is a string
            time = recipeData.time ? recipeData.time.toString() : "";

            // Initialize store with existing data
            recipeStore.set(recipeData);
        } else {
            // If creating new recipe, initialize with defaults
            category = "Velg kategori";
            region = "Velg region";
            
            recipeStore.set({
                recipeName: "",
                origin: "",
                category: "",
                portion: 0,
                region: "",
                time: "",
                ingredients: [],
                steps: [],
                notes: [],
            });
        }
    });

// Update store when values change, ensuring placeholders don't get saved
    $: if (recipeName) updateRecipeStore("recipeName", recipeName);
    $: if (origin) updateRecipeStore("origin", origin);
    $: if (portion) updateRecipeStore("portion", parseInt(portion) || 1);
    
    // For category, only update if it's not the placeholder
    $: {
        // Make sure we're not saving the placeholder text
        const actualCategory = category === "Velg kategori" ? "" : category;
        updateRecipeStore("category", actualCategory);
    }
    
    // For region, only update if it's not the placeholder
    $: {
        // Make sure we're not saving the placeholder text
        const actualRegion = region === "Velg region" ? "" : region;
        updateRecipeStore("region", actualRegion);
    }
    
    $: if (time !== undefined) updateRecipeStore("time", time); // Always update time as string
</script>

<section class="section-card">
    <h3 class="section-title">Informasjon</h3>

    <div class="form-row">
        <div class="input-with-icon">
            <svg class="input-icon" viewBox="0 0 24 24" stroke="var(--icon-color)" stroke-width="2" fill="none">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <polyline points="14 2 14 8 20 8"></polyline>
                <line x1="16" y1="13" x2="8" y2="13"></line>
                <line x1="16" y1="17" x2="8" y2="17"></line>
                <line x1="10" y1="9" x2="8" y2="9"></line>
            </svg>
            <input
                type="text"
                class="input-field"
                placeholder="Legg til navn"
                bind:value={recipeName}
            />
        </div>
    </div>

    <div class="form-row">
        <div class="input-with-icon">
            <svg class="input-icon" viewBox="0 0 24 24" stroke="var(--icon-color)" stroke-width="2" fill="none">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="2" y1="12" x2="22" y2="12"></line>
                <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
            </svg>
            <input
                type="text"
                class="input-field"
                placeholder="Legg til opphav"
                bind:value={origin}
            />
        </div>
    </div>

    <div class="form-row">
        <div class="input-with-icon">
            <svg class="input-icon" viewBox="0 0 24 24" stroke="var(--icon-color)" stroke-width="2" fill="none">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                <circle cx="9" cy="7" r="4"></circle>
                <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
            </svg>
            <input
                type="number"
                class="input-field"
                placeholder="Legg til porsjoner"
                bind:value={portion}
                min="1"
            />
        </div>
    </div>

    <div class="form-row">
        <div class="input-with-icon">
            <svg class="input-icon" viewBox="0 0 24 24" stroke="var(--icon-color)" stroke-width="2" fill="none">
                <circle cx="12" cy="12" r="10"></circle>
                <polyline points="12 6 12 12 16 14"></polyline>
            </svg>
            <input
                type="text"
                class="input-field"
                placeholder="Tid i minutter"
                bind:value={time}
            />
        </div>
    </div>

    <div class="form-row category-region-row">
        <div class="dropdown-with-icon">
            <svg class="dropdown-icon" viewBox="0 0 24 24" stroke="var(--icon-color)" stroke-width="2" fill="none">
                <path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"></path>
                <line x1="7" y1="7" x2="7.01" y2="7"></line>
            </svg>
            <select class="dropdown" bind:value={category}>
                <option value="Velg kategori">Velg kategori</option>
                {#each categories as cat}
                    <option value={cat}>{cat}</option>
                {/each}
            </select>
        </div>

        <div class="dropdown-with-icon">
            <svg class="dropdown-icon" viewBox="0 0 24 24" stroke="var(--icon-color)" stroke-width="2" fill="none">
                <polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"></polygon>
                <line x1="8" y1="2" x2="8" y2="18"></line>
                <line x1="16" y1="6" x2="16" y2="22"></line>
            </svg>
            <select class="dropdown" bind:value={region}>
                <option value="Velg region">Velg region</option>
                {#each regions as reg}
                    <option value={reg}>{reg}</option>
                {/each}
            </select>
        </div>
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
        align-items: stretch;
    }

    .input-with-icon, .dropdown-with-icon {
        position: relative;
        display: flex;
        align-items: center;
        width: 100%;
    }

    .input-icon, .dropdown-icon {
        position: absolute;
        left: 10px;
        width: 20px;
        height: 20px;
        z-index: 1;
    }

    .input-field {
        background-color: var(--input-background);
        border: none;
        border-radius: var(--input-radius);
        padding: 12px 15px 12px 40px;
        font-size: 16px;
        flex-grow: 1;
        height: 45px;
        width: 100%;
    }

    .input-field::placeholder {
        color: var(--text-light);
    }

    .category-region-row {
        display: flex;
        gap: 15px;
    }

    .dropdown {
        background-color: var(--primary-color);
        color: var(--text-on-primary);
        border: none;
        border-radius: var(--button-radius);
        padding: 12px 35px 12px 40px;
        font-size: 16px;
        appearance: none;
        background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
        background-repeat: no-repeat;
        background-position: right 10px center;
        background-size: 16px;
        cursor: pointer;
        height: 45px;
        flex: 1;
        width: 100%;
    }

    @media (max-width: 640px) {
        .category-region-row {
            flex-direction: column;
        }
    }
</style>