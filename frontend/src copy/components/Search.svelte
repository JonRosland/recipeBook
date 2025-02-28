<script>
    import { searchRecipeApi } from "./APIFunctions.js";

    const optionsMap = {
        category: ["Middag", "Dessert", "Suppe", "Forett", "Bakst", "Kake"],
        region: ["Asia", "Italia", "Frankrike", "Norge", "Annet"],
    };

    let keys = ["Ingredienser", ...Object.keys(optionsMap)];
    let selectedKey = keys[0];
    let selectedValue = "";
    let searchString = "";
    let searchResult = ""; // Variable to hold the search result

    // Reactive statement to update searchString
    $: searchString = JSON.stringify({ [selectedKey]: selectedValue });

    async function performSearch() {
        console.log("Search String:", searchString);
        try {
            searchResult = await searchRecipeApi(searchString);
        } catch (error) {
            console.error("Error:", error);
            searchResult = [];
        }
    }
</script>

<!-- Selection for Keys -->
<select bind:value={selectedKey}>
    {#each keys as key}
        <option value={key}>{key}</option>
    {/each}
</select>

{#if selectedKey === "Ingredienser"}
    <input
        type="text"
        bind:value={selectedValue}
        placeholder="Type ingredients..."
    />
{:else if optionsMap[selectedKey]}
    <select bind:value={selectedValue}>
        {#each optionsMap[selectedKey] as value}
            <option {value}>{value}</option>
        {/each}
    </select>
{/if}

<button on:click={performSearch}>Search</button>

<p>Search String: {searchString}</p>

{#if searchResult && searchResult.length > 0}
    <ul>
        {#each searchResult as recipe}
            <li><a href={"recipe/" + recipe._id}>{recipe.recipeName}</a></li>
        {/each}
    </ul>
{:else}
    <p>No search results found.</p>
{/if}
