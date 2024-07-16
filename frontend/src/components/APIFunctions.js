//const IP = process.env.APP_IP || 'localhost';
//const baseUrl = 'http://' + IP + ':4000/api/';
const baseUrl = 'http://10.0.0.20:6088/api/';

export async function getRecipeApi(id) {
    try {
        const response = await fetch(baseUrl + id);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return await response.json();
    } catch (error) {
        console.error("Error fetching recipe:", error);
        throw error;
    }
}

export async function getRecipesApi() {
    try {
        const response = await fetch(baseUrl);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return await response.json();
    } catch (error) {
        console.error("Error fetching recipe:", error);
        throw error;
    }
}

export async function updateRecipeApi(id, recipe) {
    try {
        const response = await fetch(baseUrl + id, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(recipe),
        });
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return await response.json();
    } catch (error) {
        console.error("Error updating recipe:", error);
        throw error;
    }
}

export async function postRecipeApi(recipe) {
    try {
        const response = await fetch(baseUrl + 'newRecipe', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(recipe),
        });
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return await response.json();
    } catch (error) {
        console.error("Error creating new recipe:", error);
        throw error;
    }
}

export async function searchRecipeApi(search) {
    try {
        const response = await fetch(baseUrl + 'search/' + search);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return await response.json();
    } catch (error) {
        console.error("Error fetching recipe:", error);
        throw error;
    }
}
