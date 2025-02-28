// APIFunctions.js - Centralized API functions
const baseUrl = 'http://10.0.0.20:6088/api/'; // for development
// const baseUrl = 'https://recipebook.riceemperor.com/api/';

// Helper function to handle common fetch operations
async function fetchWithErrorHandling(url, options = {}) {
    try {
        const response = await fetch(url, options);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return await response.json();
    } catch (error) {
        console.error(`API Error (${url}):`, error);
        throw error;
    }
}

// Get a single recipe by ID
export function getRecipeApi(id) {
    return fetchWithErrorHandling(baseUrl + id);
}

// Get all recipes
export function getRecipesApi() {
    return fetchWithErrorHandling(baseUrl);
}

// Update a recipe
export function updateRecipeApi(id, recipe) {
    return fetchWithErrorHandling(baseUrl + id, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(recipe)
    });
}

// Create a new recipe
export function postRecipeApi(recipe) {
    return fetchWithErrorHandling(baseUrl + 'newRecipe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(recipe)
    });
}

// Search for recipes
export function searchRecipeApi(search) {
    return fetchWithErrorHandling(baseUrl + 'search/' + search);
}

// Toggle favorite status (uses updateRecipeApi)
export async function toggleFavoriteApi(id, favoriteStatus) {
    // First get the current recipe
    const recipe = await getRecipeApi(id);

    // Then update only the favorite field
    recipe.favorite = favoriteStatus;

    // Send the update
    return updateRecipeApi(id, recipe);
}