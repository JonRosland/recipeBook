// pages/api/[id].js
import { addRecipe, getRecipe, updateRecipe, deleteRecipe, searchRecipe, getRecipes } from '../../server';

export async function apiId(req, res) {
    const { id } = req.query;

    switch (req.method) {
        case 'PUT':
            const data = req.body;
            if (!data) {
                res.status(400).json({ message: "No input data provided" });
                return;
            }
            const updateResponse = await updateRecipe(id, data);
            res.status(200).json(updateResponse);
            break;
        case 'GET':
            if (id) {
                const recipe = await getRecipe(id);
                if (recipe) {
                    res.status(200).json(recipe);
                } else {
                    res.status(404).json({ message: "Recipe not found" });
                }
            } else {
                // This block handles the '/api/' endpoint to get all recipes
                const recipes = await getRecipes();
                res.status(200).json(recipes);
            }
            break;
        case 'DELETE':
            // Uncomment and implement if you decide to use the DELETE method
            // const deleteResponse = await deleteRecipe(id);
            // res.status(200).json(deleteResponse);
            break;
        default:
            res.setHeader('Allow', ['GET', 'PUT', 'DELETE']);
            res.status(405).end(`Method ${req.method} Not Allowed`);
    }
}

// pages/api/search/[search].js
export async function apiSearch(req, res) {
    if (req.method !== 'GET') {
        res.status(405).end(`Method ${req.method} Not Allowed`);
        return;
    }

    const { search } = req.query;
    const searchDict = JSON.parse(search);
    const recipe = await searchRecipe(searchDict);

    if (recipe) {
        res.status(200).json(recipe);
    } else {
        res.status(404).json({ message: "Recipe not found" });
    }
}

// pages/api/newRecipe.js
export async function apiNewRecipe(req, res) {
    if (req.method !== 'POST') {
        res.status(405).end(`Method ${req.method} Not Allowed`);
        return;
    }

    const data = req.body;
    if (!data) {
        res.status(400).json({ message: "No input data provided" });
        return;
    }
    const recipeId = await addRecipe(data);
    res.status(201).json({ recipe_id: String(recipeId.insertedId) });
}

// pages/api/test.js
export function test(req, res) {
    res.status(200).json({ Connection: 'success' });
}
