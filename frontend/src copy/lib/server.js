//const { MongoClient, ObjectId } = require('mongodb');

import { MongoClient, ObjectId } from 'mongodb';

const url = 'mongodb://root:root@mongo:27017';
//const dbName = 'RecipeDB';
const client = new MongoClient(url);

async function connectToDB() {
    //try {
    //await client.connect();
    const db = client.db('RecipeDB');
    const dbRecipe = db.collection('Food');
    return dbRecipe;
    //} finally {
    //    await client.close();
    //}
}

async function getRecipe(id) {
    const dbRecipe = await connectToDB();
    const recipe = await dbRecipe.findOne({ _id: new ObjectId(String(id)) });
    if (recipe) {

        recipe._id = recipe._id.toString();
    }
    return recipe;
}

async function getRecipes() {
    const dbRecipe = await connectToDB();
    const recipesCursor = await dbRecipe.find({});
    const recipesList = await recipesCursor.toArray();
    return recipesList.map(recipe => ({ ...recipe, _id: recipe._id.toString() }));
}

async function addRecipe(recipe) {
    const dbRecipe = await connectToDB();
    const result = await dbRecipe.insertOne(recipe);
    return result.insertedId;
}

async function updateRecipe(id, data) {
    const dbRecipe = await connectToDB();
    const options = { upsert: true };
    const result = await dbRecipe.replaceOne({ "_id": new ObjectId(String(id)) }, { '$set': data });
    console.log(
        `${result.matchedCount} document(s) matched the filter, updated ${result.modifiedCount} document(s)`,
    );
    return { "message": result.modifiedCount ? "Recipe updated" : "Recipe not found" };
}

async function deleteRecipe(id) {
    const dbRecipe = await connectToDB();
    const result = await dbRecipe.deleteOne({ "_id": new ObjectId(String(id)) });
    return { "message": result.deletedCount ? "Recipe deleted" : "Recipe not found" };
}

async function searchRecipe(search) {
    const dbRecipe = await connectToDB();
    const recipesCursor = await dbRecipe.find(search);
    const recipesList = await recipesCursor.toArray();
    return recipesList.map(recipe => ({ ...recipe, _id: recipe._id.toString() }));
}

export { connectToDB, getRecipe, getRecipes, addRecipe, updateRecipe, deleteRecipe, searchRecipe };
