<script>
    const discordWebhookURL =
        "https://discord.com/api/webhooks/1212389938675322891/chtRaCXZOCucbbB4a5i2EwsU7HtUe2kPAwcUmPAEqAjkJXVA9DoTLxmXN2YHZezLOvKn";

    let description = "";
    async function postComment() {
        console.log("Posting comment:", description);
        const comment = {
            content: description,
        };
        try {
            const response = await fetch(discordWebhookURL, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(comment),
            });
            if (response.ok) {
                alert("Comment sent");
            } else {
                console.error("Error:", response.statusText);
                alert("Something went wrong");
            }
        } catch (error) {
            console.error("Fetch Error:", error);
            alert("Failed to send comment");
            description = "";
        }
    }
</script>

<input bind:value={description} placeholder="Forslag til forbedring" />
<button on:click={() => postComment()}>Send</button>
