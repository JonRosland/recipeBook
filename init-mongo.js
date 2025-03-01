// mongodb/init-mongo.js
db = db.getSiblingDB('admin');
// This ensures that the recipeuser can access the recipeDB
db.createUser({
  user: process.env.MONGO_USERNAME,
  pwd: process.env.MONGO_PASSWORD,
  roles: [
    { role: "readWrite", db: process.env.MONGO_DATABASE },
    { role: "dbAdmin", db: process.env.MONGO_DATABASE }
  ]
});

// Initialize the recipe database
db = db.getSiblingDB(process.env.MONGO_DATABASE);
db.createCollection('recipes');