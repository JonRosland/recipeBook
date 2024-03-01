const { MongoClient, ObjectId } = require('mongodb');

async function connectToDB() {
    const uri = "mongodb://root:root@mongo:27017/";
    const client = new MongoClient(uri);

    try {
        await client.connect();
        console.log('Connected to DB');
        const db = client.db("RecipeDB");
        const db_recipe = db.collection("Food");
        return { db_recipe, client };
    } catch (error) {
        console.error('Could not connect to DB', error);
        throw error;
    }
}

async function getRecipe(id) {
    const { db_recipe, client } = await connectToDB();
    try {
        const recipe = await db_recipe.findOne({ "_id": ObjectId(id) });
        if (recipe) {
            recipe._id = recipe._id.toString();
        }
        return recipe;
    } finally {
        client.close();
    }
}

async function getRecipes() {
    const { db_recipe, client } = await connectToDB();
    try {
        const recipes_cursor = await db_recipe.find().toArray();
        recipes_cursor.forEach(recipe => {
            recipe._id = recipe._id.toString();
        });
        return recipes_cursor;
    } finally {
        client.close();
    }
}

async function deleteRecipe(id) {
    const { db_recipe, client } = await connectToDB();
    try {
        const response = await db_recipe.deleteOne({ "_id": ObjectId(id) });
        return response.deletedCount ? { "message": "Recipe deleted" } : { "message": "Recipe not found" };
    } finally {
        client.close();
    }
}

async function updateRecipe(id, data) {
    const { db_recipe, client } = await connectToDB();
    try {
        delete data._id; // Ensure _id is not in update data
        const response = await db_recipe.updateOne({ "_id": ObjectId(id) }, { '$set': data });
        return response.modifiedCount ? { "message": "Recipe updated" } : { "message": "Recipe not found" };
    } finally {
        client.close();
    }
}

async function addRecipe(recipe) {
    const { db_recipe, client } = await connectToDB();
    try {
        const response = await db_recipe.insertOne(recipe);
        return response.insertedId;
    } finally {
        client.close();
    }
}

async function searchRecipe(search) {
    const { db_recipe, client } = await connectToDB();
    try {
        const recipes_cursor = await db_recipe.find(search).toArray();
        recipes_cursor.forEach(recipe => {
            recipe._id = recipe._id.toString();
        });
        return recipes_cursor;
    } finally {
        client.close();
    }
}

// Function to dump recipes as JSON is not directly translated
// because Node.js environment and file system handling differ from Python.
// You would typically use the `fs` module to write files in Node.js.

// Example usage of async functions
(async () => {
    try {
        const recipe = await getRecipe('your_recipe_id_here');
        console.log(recipe);
    } catch (error) {
        console.error('Error:', error);
    }
})();
