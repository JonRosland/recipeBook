<script>
    import {
        recipeStore,
        updateRecipeStore,
        isRecipeStore,
        swapElementsStore,
        deleteElementStore,
    } from "../../stores/recipeStore.js";
    import Button from "../Button.svelte";

    export let title = "";
    export let element = "";

    let newValue;
    if (element === "ingredients") {
        newValue = { name: "", quantity: null, unit: "" };
    } else {
        newValue = "";
    }

    function updateElement() {
        updateRecipeStore(element, newValue);
        if (element === "ingredients") {
            newValue = { name: "", quantity: null, unit: "" };
        } else {
            newValue = "";
        }
    }

    let view = [];
    $: if ($isRecipeStore) {
        view = $recipeStore[element];
    }

    function swap(currentIndex, newIndex) {
        if (newIndex >= 0 && newIndex < view.length) {
            swapElementsStore(element, currentIndex, newIndex);
        }
    }
</script>

<section class={element}>
    <h3>{title}</h3>
    <div>
        {#if element == "ingredients"}
            <input bind:value={newValue.name} placeholder="Ingrediens" />
            <input
                type="number"
                bind:value={newValue.quantity}
                placeholder="Mengde"
            />
            <input bind:value={newValue.unit} placeholder="Enhet" />
        {:else}
            <input bind:value={newValue} placeholder={"Legg til " + title} />
        {/if}
        <Button label={"Legg til " + title} onClick={updateElement} />
    </div>
    <div class="textLeft">
        <ul>
            {#if element == "ingredients"}
                {#each view as item, index}
                    <li>
                        {item.name}
                        {item.quantity}{item.unit}
                        <button
                            on:click={() => swap(index, index - 1)}
                            disabled={index === 0}>↑</button
                        >
                        <button
                            on:click={() => swap(index, index + 1)}
                            disabled={index === view.length - 1}>↓</button
                        >
                        <button
                            on:click={() => deleteElementStore(element, index)}
                            >slett</button
                        >
                    </li>
                {/each}
            {:else}
                {#each view as item, index}
                    <li>
                        {item}
                        <button
                            on:click={() => swap(index, index - 1)}
                            disabled={index === 0}>↑</button
                        >
                        <button
                            on:click={() => swap(index, index + 1)}
                            disabled={index === view.length - 1}>↓</button
                        >
                        <button
                            on:click={() => deleteElementStore(element, index)}
                            >slett</button
                        >
                    </li>
                {/each}
            {/if}
        </ul>
    </div>
</section>

<style>
    section {
        border: 1px solid black;
        margin: 0 1em 1em 0;
        padding: 1em;
        box-sizing: border-box;
        flex: 2 1 40%; /* Grow to 40% of the container's width */
        min-width: 300px; /* Minimum width before wrapping */
    }
</style>
