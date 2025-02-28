<script>
    import Improvement from "../Improvement.svelte";
    import {
        updateRecipeApi,
        getRecipeApi,
        postRecipeApi,
    } from "../APIFunctions.js";
    import Button from "../Button.svelte";
    import {
        isRecipeStore,
        setRecipeStore,
        getRecipeStore,
    } from "../../stores/recipeStore.js";

    export let id = "";
    export let locationn = "";

    let newRecipe = {
        recipeName: "Oppskrift Navn",
        origin: "Feks Mor",
        category: "",
        portion: 0,
        region: "",
        ingredients: [],
        steps: [],
        notes: [],
    };
    let editRecipe = {};

    async function setRecipe() {
        editRecipe = await getRecipeApi(id);
        await setRecipeStore(editRecipe);
        isRecipeStore.set(true);
    }
    async function setNewRecipe() {
        await setRecipeStore(newRecipe);
        isRecipeStore.set(true);
    }

    if (id) {
        setRecipe();
    } else if (!id) {
        setNewRecipe();
    }

    async function saveRecipe() {
        let newRecipe = getRecipeStore();
        if (id) {
            await updateRecipeApi(editRecipe._id, newRecipe);
            alert("Oppskrift oppdatert");
        } else if (!id) {
            const idRecipe = await postRecipeApi(newRecipe);
            alert("Oppskrift lagret med id: " + idRecipe.recipe_id);
            window.location.href = "/edit/" + idRecipe.recipe_id;
        }
    }
    async function backToRecipe() {
        window.location.href = "/recipe/" + editRecipe._id;
    }
    function redirectAllRecipes() {
        window.location.href = "/";
    }
</script>

<div class="save">
    <Button label="Lagre endringer" onClick={saveRecipe} />
    <Button label="Tilbake til alle oppskrifer" onClick={redirectAllRecipes} />
    {#if id}
        <Button
            label="Tilbake til {editRecipe.recipeName}"
            onClick={backToRecipe}
        />{/if}
    <Improvement client:load location={locationn} />
</div>
