# RecipeBook Frontend Guide

## Build & Development Commands
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build locally
- `npm run deno-deploy` - Build and deploy to Deno

    ## Project Structure
    - Astro + Svelte frontend with Deno server adapter
    - MongoDB for database (connected via API)

    ## Code Style Guidelines
    - Centralize API calls in APIFunctions.js
    - Store state management in stores/ directory (using nanostores)
    - Prefer minimal and simple code
    - Utalize modualr programming

    ## Naming Conventions
    - PascalCase for everyting
    - Use descriptive function names that indicate purpose
    - Suffix API functions with "Api" (e.g., getRecipeApi)