// Define the base URL for API calls
const getApiUrl = () => {
    // Check if we're in a browser context
    const isBrowser = typeof window !== 'undefined';
    
    // Always use relative URL for browser requests - this will be handled by our proxy
    if (isBrowser) {
        console.log('Browser context detected, using relative URL /api/');
        return '/api/';
    }
    
    // For server-side rendering with Vite (build time)
    if (typeof import.meta !== 'undefined' && import.meta.env) {
        // Use SERVER_API_URL for direct container-to-container communication
        if (import.meta.env.SERVER_API_URL) {
            console.log(`Server context, using import.meta.env.SERVER_API_URL: ${import.meta.env.SERVER_API_URL}`);
            return import.meta.env.SERVER_API_URL;
        }
        
        // Fallback to PUBLIC_API_URL
        console.log(`Server context, using import.meta.env.PUBLIC_API_URL: ${import.meta.env.PUBLIC_API_URL}`);
        return import.meta.env.PUBLIC_API_URL;
    }
    
    // For server-side rendering with Deno (runtime)
    if (typeof Deno !== 'undefined' && Deno.env && Deno.env.get) {
        // Use SERVER_API_URL for direct container-to-container communication
        const serverUrl = Deno.env.get("SERVER_API_URL");
        if (serverUrl) {
            console.log(`Server context, using Deno.env SERVER_API_URL: ${serverUrl}`);
            return serverUrl;
        }
        
        const publicUrl = Deno.env.get("PUBLIC_API_URL");
        if (publicUrl) {
            console.log(`Server context, using Deno.env PUBLIC_API_URL: ${publicUrl}`);
            return publicUrl;
        }
    }
    
    // Final fallback - use internal Docker network URL for server, relative URL for browser
    const defaultUrl = isBrowser ? '/api/' : 'http://backend:6088/api/';
    console.log(`Using default URL: ${defaultUrl}`);
    return defaultUrl;
};

const baseUrl = getApiUrl();
console.log(`API URL being used: ${baseUrl}`);

/**
 * Fetch a specific recipe by ID
 * @param {string} id - Recipe ID
 * @returns {Promise<Object>} Recipe data
 */
export async function getRecipeApi(id) {
    try {
        // Sanitize id - remove any unwanted characters
        const sanitizedId = id.trim();
        
        console.log(`Fetching recipe from: ${baseUrl}${sanitizedId}`);
        
        // First check the backend health to ensure connection is working
        try {
            const healthCheck = await fetch(`${baseUrl}health`);
            const healthData = await healthCheck.json();
            console.log(`API health check result:`, healthData);
        } catch (healthError) {
            console.warn("Health check failed, but continuing with recipe fetch:", healthError);
        }
        
        const response = await fetch(`${baseUrl}${sanitizedId}`);
        
        // Log the entire response for debugging
        console.log(`Recipe fetch response status: ${response.status}`);
        
        // Handle 404 specifically to provide better error message
        if (response.status === 404) {
            console.log(`Recipe with ID ${sanitizedId} not found`);
            
            // Check database health to see collection information
            try {
                console.log("Running DB health check to diagnose the issue...");
                const dbHealthCheck = await fetch(`${baseUrl}db-health`);
                const dbHealthData = await dbHealthCheck.json();
                console.log("DB Health check result:", dbHealthData);
            } catch (dbError) {
                console.warn("DB health check failed:", dbError);
            }
            
            throw new Error(`Recipe not found: ${sanitizedId}`);
        }
        
        if (!response.ok) {
            throw new Error(`Network response was not ok: ${response.status} ${response.statusText}`);
        }
        
        const recipe = await response.json();
        console.log(`Recipe fetch successful, recipe:`, recipe);
        
        return recipe;
    } catch (error) {
        console.error("Error fetching recipe:", error);
        throw error;
    }
}

/**
 * Fetch all recipes with retry capability
 * @param {number} retries - Number of retry attempts (default: 2)
 * @returns {Promise<Array>} Array of recipes
 */
export async function getRecipesApi(retries = 2) {
    let lastError;
    
    for (let attempt = 0; attempt <= retries; attempt++) {
        try {
            console.log(`Fetching all recipes from: ${baseUrl} (attempt ${attempt + 1}/${retries + 1})`);
            
            const response = await fetch(baseUrl, {
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                cache: 'no-cache'
            });
            
            if (!response.ok) {
                const errorText = await response.text().catch(() => 'No error details');
                throw new Error(`Network response was not ok: ${response.status} ${response.statusText}. Details: ${errorText}`);
            }
            
            const data = await response.json();
            console.log(`Successfully fetched ${data.length || 0} recipes`);
            return data;
        } catch (error) {
            console.error(`Error fetching recipes (attempt ${attempt + 1}/${retries + 1}):`, error);
            lastError = error;
            
            if (attempt < retries) {
                // Wait an increasing amount of time before retrying (exponential backoff)
                const waitTime = Math.min(1000 * Math.pow(2, attempt), 8000);
                console.log(`Retrying in ${waitTime}ms...`);
                await new Promise(resolve => setTimeout(resolve, waitTime));
            }
        }
    }
    
    // All retry attempts failed
    throw lastError || new Error('Failed to fetch recipes after multiple attempts');
}

/**
 * Update an existing recipe
 * @param {string} id - Recipe ID
 * @param {Object} recipe - Updated recipe data
 * @returns {Promise<Object>} Updated recipe data
 */
export async function updateRecipeApi(id, recipe) {
    try {
        // Clone the recipe object to avoid modifying the original
        const recipeData = { ...recipe };
        
        // Map recipeName to title if needed for API compatibility
        if (recipeData.recipeName && !recipeData.title) {
            recipeData.title = recipeData.recipeName;
            console.log("Mapped recipeName to title for API compatibility");
        }
        
        console.log(`Updating recipe at: ${baseUrl}${id}`);
        console.log("Recipe data:", JSON.stringify(recipeData));
        
        const response = await fetch(`${baseUrl}${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(recipeData),
        });
        
        // Log response for debugging
        console.log(`Response status: ${response.status}`);
        
        // Handle specific status codes
        if (response.status === 404) {
            throw new Error(`Recipe not found: ${id}`);
        }
        
        if (!response.ok) {
            const responseText = await response.text().catch(() => 'No error details');
            throw new Error(`Network response was not ok: ${response.status} ${response.statusText}. Details: ${responseText}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error("Error updating recipe:", error);
        throw error;
    }
}

/**
 * Create a new recipe
 * @param {Object} recipe - New recipe data
 * @param {number} retries - Number of retry attempts (default: 1)
 * @returns {Promise<Object>} Created recipe data
 */
export async function postRecipeApi(recipe, retries = 1) {
    // Clone the recipe object to avoid modifying the original
    const recipeData = { ...recipe };
    
    // Map recipeName to title if needed for API compatibility
    if (recipeData.recipeName && !recipeData.title) {
        recipeData.title = recipeData.recipeName;
        console.log("Mapped recipeName to title for API compatibility");
    }
    
    // Ensure required fields have values
    const requiredFields = ['title', 'ingredients', 'steps'];
    const missingFields = requiredFields.filter(field => !recipeData[field]);
    
    if (missingFields.length > 0) {
        throw new Error(`Missing required fields: ${missingFields.join(', ')}`);
    }
    
    // Ensure ingredients is an array
    if (!Array.isArray(recipeData.ingredients)) {
        recipeData.ingredients = recipeData.ingredients ? [recipeData.ingredients] : [];
    }
    
    // Ensure steps is an array
    if (!Array.isArray(recipeData.steps)) {
        recipeData.steps = recipeData.steps ? [recipeData.steps] : [];
    }
    
    // Ensure time is a string if present
    if (recipeData.time !== undefined && recipeData.time !== null) {
        recipeData.time = String(recipeData.time);
    }
    
    console.log(`Creating new recipe at: ${baseUrl}newRecipe`);
    console.log("Recipe data:", JSON.stringify(recipeData));
    
    let lastError;
    
    for (let attempt = 0; attempt <= retries; attempt++) {
        try {
            console.log(`Sending POST request (attempt ${attempt + 1}/${retries + 1})`);
            
            const response = await fetch(`${baseUrl}newRecipe`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify(recipeData),
            });
            
            console.log(`Response status: ${response.status}`);
            
            // Try to parse the response or get text for debugging
            let responseData;
            const responseText = await response.text();
            console.log(`Response text: ${responseText}`);
            
            try {
                responseData = JSON.parse(responseText);
            } catch (e) {
                console.warn("Could not parse response as JSON", e);
                responseData = { message: responseText };
            }
            
            // Handle different error status codes
            if (response.status === 400) {
                throw new Error(`Bad request: ${responseData.message || "Data validation failed"}`);
            } else if (response.status === 500) {
                throw new Error(`Server error: ${responseData.message || "Internal server error"}`);
            } else if (!response.ok) {
                throw new Error(`Network error (${response.status}): ${responseText}`);
            }
            
            console.log("Successfully created recipe:", responseData);
            return responseData;
        } catch (error) {
            console.error(`Error creating recipe (attempt ${attempt + 1}/${retries + 1}):`, error);
            lastError = error;
            
            // Don't retry client-side validation errors
            if (error.message.includes("Missing required fields")) {
                throw error;
            }
            
            if (attempt < retries) {
                const waitTime = Math.min(1000 * Math.pow(2, attempt), 4000);
                console.log(`Retrying in ${waitTime}ms...`);
                await new Promise(resolve => setTimeout(resolve, waitTime));
            }
        }
    }
    
    // All retry attempts failed
    throw lastError || new Error('Failed to create recipe after multiple attempts');
}

/**
 * Search for recipes
 * @param {string} search - Search string (JSON format)
 * @returns {Promise<Array>} Array of matching recipes
 */
export async function searchRecipeApi(search) {
    try {
        console.log(`Searching recipes at: ${baseUrl}search/${search}`);
        
        // Handle possible comma-separated ingredients
        let searchObj;
        try {
            searchObj = JSON.parse(search);
            
            // Special handling for ingredients search
            if (searchObj.ingredients && Array.isArray(searchObj.ingredients)) {
                // Already handled in SearchBar.svelte
            }
            
            // Handle favorites search
            if (searchObj.favorite === true) {
                console.log("Searching for favorite recipes");
            }
            
            // Handle name search
            if (searchObj.recipeName) {
                console.log(`Searching for recipes with name: ${searchObj.recipeName}`);
            }
            
            // Handle origin search
            if (searchObj.origin) {
                console.log(`Searching for recipes with origin: ${searchObj.origin}`);
            }
            
        } catch (e) {
            console.error("Error parsing search JSON:", e);
        }
        
        const response = await fetch(`${baseUrl}search/${search}`);
        
        if (!response.ok) {
            throw new Error(`Network response was not ok: ${response.status} ${response.statusText}`);
        }
        
        const results = await response.json();
        return results;
    } catch (error) {
        console.error("Error searching recipes:", error);
        throw error;
    }
}

/**
 * Toggle favorite status of a recipe
 * @param {string} id - Recipe ID
 * @param {boolean} isFavorite - New favorite status
 * @returns {Promise<Object>} Updated recipe data
 */
export async function toggleFavoriteApi(id, isFavorite) {
    try {
        // First, get the current recipe
        const recipe = await getRecipeApi(id);

        // Update the favorite status
        recipe.favorite = isFavorite;

        // Save the updated recipe
        const response = await updateRecipeApi(id, recipe);

        return response;
    } catch (error) {
        console.error("Error toggling favorite status:", error);
        throw error;
    }
}

/**
 * Check API health 
 * @returns {Promise<boolean>} True if API is healthy
 */
export async function checkApiHealth() {
    try {
        console.log(`Checking API health at: ${baseUrl}health`);
        const response = await fetch(`${baseUrl}health`);
        
        if (!response.ok) {
            return false;
        }
        
        const data = await response.json();
        return data.status === 'healthy';
    } catch (error) {
        console.error("API health check failed:", error);
        return false;
    }
}