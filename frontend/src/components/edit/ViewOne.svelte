<script>
    import {
        recipeStore,
        updateRecipeStore,
        isRecipeStore,
    } from "../../stores/recipeStore.js";
    import Button from "../Button.svelte";

    export let title = "";
    export let element = "";
    const _categories = [
        "Middag",
        "Dessert",
        "Suppe",
        "Forett",
        "Bakst",
        "Kake",
    ];
    const _region = ["Asia", "Italia", "Frankrike", "Norge", "Annet"];
    let newValue = "";
    function updateElement() {
        updateRecipeStore(element, newValue);
        newValue = "";
    }

    let view = [];
    $: if ($isRecipeStore) {
        view = $recipeStore[element];
    }

    $: if (element === "category" || element === "region") {
        newValue = view;
    }

    $: if (newValue && (element === "category" || element === "region")) {
        updateRecipeStore(element, newValue);
    }
</script>

<section class={element}>
    <h3>{title}</h3>
    <div>
        {#if element === "category"}
            <select bind:value={newValue}>
                {#each _categories as val}
                    <option value={val}>{val}</option>
                {/each}
            </select>
        {:else if element === "region"}
            <select bind:value={newValue}>
                {#each _region as val}
                    <option value={val}>{val}</option>
                {/each}
            </select>
        {:else}
            <input bind:value={newValue} placeholder={"Legg til " + title} />
            <Button label={"Legg til " + title} onClick={updateElement} />
            <div class="textLeft">
                <h4>{view}</h4>
            </div>
        {/if}
    </div>
</section>

<style>
    section {
        border: 1px solid black;
        margin: 0 1em 1em 0;
        padding: 1em;
        box-sizing: border-box;
        flex: 2 1 40%;
        min-width: 300px;
    }
</style>
