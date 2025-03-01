// Add a Deno shim if running in Node
if (typeof Deno === 'undefined') {
    globalThis.Deno = {
      env: {
        get: (key) => process.env[key],
      },
    };
}
  
import { defineConfig } from 'astro/config';
import svelte from '@astrojs/svelte';
import deno from "@astrojs/deno";
  
// Get environment variables with fallbacks for build and runtime
const PUBLIC_API_URL = Deno.env.get("PUBLIC_API_URL") || "http://backend:6088/api/";
const PUBLIC_ENABLE_FAVORITES = Deno.env.get("PUBLIC_ENABLE_FAVORITES") || "true";
const PUBLIC_ENABLE_SEARCH = Deno.env.get("PUBLIC_ENABLE_SEARCH") || "true";
const PUBLIC_THEME = Deno.env.get("PUBLIC_THEME") || "light";
const PUBLIC_ITEMS_PER_PAGE = Deno.env.get("PUBLIC_ITEMS_PER_PAGE") || "12";

export default defineConfig({
  integrations: [svelte()],
  output: 'server',
  adapter: deno({
    // Deno adapter options - Don't start a server, we use run-server.mjs
    port: 8085,
    start: false,
  }),
  // Disable image processing with Sharp
  image: {
    service: { entrypoint: 'astro/assets/services/noop' },
  },
  // Add Vite config for environment variables
  vite: {
    // Ensure environment variables are available during build and runtime
    define: {
      'import.meta.env.PUBLIC_API_URL': JSON.stringify(PUBLIC_API_URL),
      'import.meta.env.PUBLIC_ENABLE_FAVORITES': JSON.stringify(PUBLIC_ENABLE_FAVORITES),
      'import.meta.env.PUBLIC_ENABLE_SEARCH': JSON.stringify(PUBLIC_ENABLE_SEARCH),
      'import.meta.env.PUBLIC_THEME': JSON.stringify(PUBLIC_THEME),
      'import.meta.env.PUBLIC_ITEMS_PER_PAGE': JSON.stringify(PUBLIC_ITEMS_PER_PAGE),
    },
    // This helps with Deno compatibility
    server: {
      hmr: {
        clientPort: Deno.env.get("HMR_CLIENT_PORT") || 3000,
      },
    },
  },
});
  