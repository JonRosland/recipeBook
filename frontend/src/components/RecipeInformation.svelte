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
            category = recipeData.category || "";
            region = recipeData.region || "";
            time = recipeData.time ? recipeData.time.toString() : "";

            // Initialize store with existing data
            recipeStore.set(recipeData);
        } else {
            // If creating new recipe, initialize with defaults
            recipeStore.set({
                recipeName: "",
                origin: "",
                category: "",
                portion: 0,
                region: "",
                ingredients: [],
                steps: [],
                notes: [],
            });
        }
    });

    // Update store when values change
    $: if (recipeName) updateRecipeStore("recipeName", recipeName);
    $: if (origin) updateRecipeStore("origin", origin);
    $: if (portion) updateRecipeStore("portion", parseInt(portion) || 1);
    $: if (category) updateRecipeStore("category", category);
    $: if (region) updateRecipeStore("region", region);
    $: if (time) updateRecipeStore("time", time);
</script>

<section class="section-card">
    <h3 class="section-title">Informasjon</h3>

    <div class="form-row">
        <input
            type="text"
            class="input-field"
            placeholder="Legg til navn"
            bind:value={recipeName}
        />
    </div>

    <div class="form-row">
        <input
            type="text"
            class="input-field"
            placeholder="Legg til opphav"
            bind:value={origin}
        />
    </div>

    <div class="form-row">
        <input
            type="number"
            class="input-field"
            placeholder="Legg til porsjoner"
            bind:value={portion}
            min="1"
        />
    </div>

    <div class="form-row">
        <input
            type="text"
            class="input-field"
            placeholder="Tid i minutter"
            bind:value={time}
        />
    </div>

    <div class="form-row category-region-row">
        <select class="dropdown" bind:value={category}>
            <option value="">Velg kategori</option>
            {#each categories as cat}
                <option value={cat}>{cat}</option>
            {/each}
        </select>

        <select class="dropdown" bind:value={region}>
            <option value="">Velg region</option>
            {#each regions as reg}
                <option value={reg}>{reg}</option>
            {/each}
        </select>
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

    .input-field {
        background-color: var(--input-background);
        border: none;
        border-radius: var(--input-radius);
        padding: 12px 15px;
        font-size: 16px;
        flex-grow: 1;
        height: 45px;
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
        padding: 12px 35px 12px 15px;
        font-size: 16px;
        appearance: none;
        background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
        background-repeat: no-repeat;
        background-position: right 10px center;
        background-size: 16px;
        cursor: pointer;
        height: 45px;
        flex: 1;
    }
</style>
