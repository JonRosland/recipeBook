// This is a sample modification for your Deno entry point
// You'll need to adapt this to your actual entry file

import { handler as ssrHandler } from '../dist/server/entry.mjs';

// Attempt to load .env.production if it exists
try {
    const { load } = await import("https://deno.land/std/dotenv/mod.ts");
    await load({ export: true, envPath: "./.env.production" });
    console.log("Loaded environment variables from .env.production");
} catch (err) {
    console.log("No .env file loaded or error loading .env file");
    // Continue anyway - we'll use defaults or system environment variables
}

// Create your server
Deno.serve({
    port: parseInt(Deno.env.get("PORT") || "8000"),
}, async (request) => {
    // Pass the environment variables to the SSR handler context if needed
    const envVars = {
        PUBLIC_API_URL: Deno.env.get("PUBLIC_API_URL") || "/api/",
        PUBLIC_ENABLE_FAVORITES: Deno.env.get("PUBLIC_ENABLE_FAVORITES") || "true",
        PUBLIC_ENABLE_SEARCH: Deno.env.get("PUBLIC_ENABLE_SEARCH") || "true",
        PUBLIC_THEME: Deno.env.get("PUBLIC_THEME") || "light",
        PUBLIC_ITEMS_PER_PAGE: Deno.env.get("PUBLIC_ITEMS_PER_PAGE") || "12",
    };

    // You may need to modify this depending on your exact setup
    return ssrHandler(request, { env: envVars });
});