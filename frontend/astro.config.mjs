import { defineConfig } from 'astro/config';
import svelte from '@astrojs/svelte';
import deno from "@astrojs/deno";
//import deno from "deno-astro-adapter";

export default defineConfig({
    integrations: [svelte(), deno()],
    output: 'server',
    adapter: deno(),
});
