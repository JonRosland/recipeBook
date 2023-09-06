import { MongoClient } from 'mongodb';

async function connectDB() {
  try {
    const client = new MongoClient('mongo://localhost:27017', { useUnifiedTopology: true });
    await client.connect();
    const db = client.db('cookbookdb');
    console.log('Connected to the database');
    db.recipes.insert({ name: "Test Recipe", ingredients: ["ingredient1", "ingredient2"], instructions: "Some instructions here." })

    
    return db;
  } catch (err) {
    console.error('Failed to connect to the database', err);
  }
}

export default connectDB;