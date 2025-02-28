<script>
    export let label = "";
    export let onClick = () => {};
</script>

<button on:click={onClick}>
    {label}
</button>

<style>
    button {
        border-radius: 4px;
        cursor: pointer;
    }
    button:hover {
        color: var(--btn-color--hover, var(--gray12));
        border-color: var(--btn-bd--hover, transparent);
        background-color: var(--btn-bg--hover, var(--gray4));
    }
</style>
