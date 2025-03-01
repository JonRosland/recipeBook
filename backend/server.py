from pymongo import MongoClient
from bson.objectid import ObjectId
import json
import os
import logging
from typing import Tuple, List, Dict, Any, Optional
from functools import wraps
from dotenv import load_dotenv

# Load environment variables
load_dotenv()  # This will load from .env by default

# Configure logging
log_level = os.getenv('LOG_LEVEL', 'info').upper()
log_file = os.getenv('LOG_FILE_PATH', 'app.log')
log_format = os.getenv('LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create logs directory if it doesn't exist
os.makedirs(os.path.dirname(log_file), exist_ok=True)

logging.basicConfig(
    level=getattr(logging, log_level, logging.INFO),
    format=log_format,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(log_file)
    ]
)
logger = logging.getLogger(__name__)

class DatabaseError(Exception):
    """Custom exception for database operations."""
    pass

def db_connection(func):
    """Decorator to handle database connections and errors."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        client = None
        try:
            client = get_db_client()
            db = client["RecipeDB"]
            db_recipe = db["Food"]
            result = func(db_recipe, *args, **kwargs)
            return result
        except Exception as e:
            logger.error(f"Database error in {func.__name__}: {str(e)}")
            raise DatabaseError(f"Database operation failed: {str(e)}")
        finally:
            if client:
                client.close()
    return wrapper

def get_db_client() -> MongoClient:
    """Create and return a MongoDB client with error handling."""
    try:
        # Get database connection parameters from environment variables
        db_host = os.getenv('DB_HOST', 'localhost')
        db_port = int(os.getenv('DB_PORT', '27017'))
        db_user = os.getenv('DB_USER', 'root')
        db_pass = os.getenv('DB_PASS', 'root')
        db_uri = os.getenv('MONGODB_URI')
        db_timeout_ms = int(os.getenv('DB_TIMEOUT_MS', '5000'))
        
        if db_uri:
            logger.info(f"Connecting to MongoDB using URI (host masked)")
            client = MongoClient(
                db_uri,
                serverSelectionTimeoutMS=db_timeout_ms
            )
        else:
            logger.info(f"Connecting to MongoDB at {db_host}:{db_port}")
            client = MongoClient(
                host=db_host, 
                port=db_port,
                username=db_user,
                password=db_pass,
                serverSelectionTimeoutMS=db_timeout_ms
            )
        
        # Verify connection
        client.server_info()
        return client
    except Exception as e:
        logger.error(f"Failed to connect to database: {str(e)}")
        raise DatabaseError(f"Failed to connect to database: {str(e)}")

def _format_recipe(recipe: Dict) -> Dict:
    """Convert ObjectId to string in recipe document."""
    if recipe and '_id' in recipe:
        recipe['_id'] = str(recipe['_id'])
    return recipe

@db_connection
def getRecipe(db_recipe, id: str) -> Optional[Dict]:
    """Get a single recipe by ID."""
    try:
        # Get database collection information from environment variables
        collection_name = os.getenv('RECIPE_COLLECTION_NAME', 'recipes')
        db_name = os.getenv('MONGO_DATABASE', 'recipeDB')
        
        logger.info(f"Looking up recipe with ID: {id}")
        logger.info(f"Current collection: {db_recipe.name}, Target collection: {collection_name}")
        logger.info(f"Current database: {db_recipe.database.name}, Target database: {db_name}")
        
        # Get database client
        client = db_recipe.database.client
        
        # CRITICAL FIX: Use case-insensitive comparison for database name
        actual_db_name = db_recipe.database.name
        if actual_db_name.lower() != db_name.lower():
            logger.warning(f"Database name case mismatch: current '{actual_db_name}', expected '{db_name}'")
            # Just use the actual database rather than trying to switch
            db = db_recipe.database
        else:
            db = db_recipe.database
        
        # Try to find the recipe in the current collection first
        try:
            recipe = db_recipe.find_one({"_id": ObjectId(id)})
            if recipe:
                logger.info(f"Recipe found in collection '{db_recipe.name}' with ID: {id}")
                return _format_recipe(recipe)
        except Exception as e:
            logger.error(f"Error finding recipe in '{db_recipe.name}': {str(e)}")
        
        # If not found, try other collections that might contain recipes
        potential_collections = ['recipes', 'Food']
        if db_recipe.name not in potential_collections:
            potential_collections.append(db_recipe.name)
        
        # Try each collection
        for coll_name in potential_collections:
            if coll_name != db_recipe.name:  # Skip the one we already tried
                try:
                    coll = db[coll_name]
                    recipe = coll.find_one({"_id": ObjectId(id)})
                    if recipe:
                        logger.info(f"Recipe found in alternate collection '{coll_name}' with ID: {id}")
                        return _format_recipe(recipe)
                except Exception as e:
                    logger.error(f"Error finding recipe in '{coll_name}': {str(e)}")
        
        # If we got here, no recipe was found
        logger.warning(f"No recipe found with ID: {id} in any collection")
        return None
    except Exception as e:
        logger.error(f"Error retrieving recipe {id}: {str(e)}")
        raise

@db_connection
def getRecipes(db_recipe) -> List[Dict]:
    """Get all recipes."""
    try:
        recipes_cursor = db_recipe.find()
        recipes_list = list(recipes_cursor)
        return [_format_recipe(recipe) for recipe in recipes_list]
    except Exception as e:
        logger.error(f"Error retrieving all recipes: {str(e)}")
        raise

@db_connection
def deleteRecipe(db_recipe, id: str) -> Dict:
    """Delete a recipe by ID."""
    try:
        response = db_recipe.delete_one({"_id": ObjectId(id)})
        return {"message": "Recipe deleted", "deleted": True} if response.deleted_count else {"message": "Recipe not found", "deleted": False}
    except Exception as e:
        logger.error(f"Error deleting recipe {id}: {str(e)}")
        raise

@db_connection
def updateRecipe(db_recipe, id: str, data: Dict) -> Dict:
    """Update a recipe by ID."""
    try:
        # Make a copy to avoid modifying the original
        update_data = data.copy()
        # Remove _id if present to avoid MongoDB error
        if '_id' in update_data:
            update_data.pop('_id')
            
        response = db_recipe.update_one({"_id": ObjectId(id)}, {'$set': update_data})
        return {
            "message": "Recipe updated", 
            "updated": True,
            "modified_count": response.modified_count
        } if response.modified_count else {
            "message": "Recipe not found or no changes made", 
            "updated": False,
            "modified_count": 0
        }
    except Exception as e:
        logger.error(f"Error updating recipe {id}: {str(e)}")
        raise

@db_connection
def addRecipe(db_recipe, recipe: Dict) -> str:
    """Add a new recipe."""
    try:
        logger.info("Adding new recipe")
        result = db_recipe.insert_one(recipe)
        logger.info(f"Recipe added with ID: {result.inserted_id}")
        return str(result.inserted_id)
    except Exception as e:
        logger.error(f"Error adding recipe: {str(e)}")
        raise

@db_connection
def searchRecipe(db_recipe, search: Dict) -> List[Dict]:
    """Search for recipes based on criteria."""
    try:
        recipes_cursor = db_recipe.find(search)
        recipes_list = list(recipes_cursor)
        return [_format_recipe(recipe) for recipe in recipes_list]
    except Exception as e:
        logger.error(f"Error searching recipes with criteria {search}: {str(e)}")
        raise

@db_connection
def check_db_consistency(db_recipe):
    """Check and display database and collection information."""
    try:
        # Get expected configuration from environment variables
        expected_db_name = os.getenv('MONGO_DATABASE', 'recipeDB')
        expected_collection_name = os.getenv('RECIPE_COLLECTION_NAME', 'recipes')
        
        # Get current database and collection
        current_db = db_recipe.database
        current_db_name = current_db.name
        current_collection_name = db_recipe.name
        
        logger.info("=== Database Consistency Check ===")
        logger.info(f"Expected database: {expected_db_name}, Current: {current_db_name}")
        logger.info(f"Expected collection: {expected_collection_name}, Current: {current_collection_name}")
        
        # Check all collections in the current database
        logger.info(f"Collections in database '{current_db_name}':")
        for collection_name in current_db.list_collection_names():
            collection = current_db[collection_name]
            count = collection.count_documents({})
            logger.info(f"  - {collection_name}: {count} documents")
            
            # Show sample documents from each non-empty collection
            if count > 0:
                sample = collection.find_one()
                if sample and '_id' in sample:
                    logger.info(f"    Sample ID: {sample['_id']} (type: {type(sample['_id'])})")
                    if 'title' in sample:
                        logger.info(f"    Title: {sample['title']}")
                    elif 'recipeName' in sample:
                        logger.info(f"    Recipe Name: {sample['recipeName']}")
        
        # Check for expected collection
        if expected_collection_name not in current_db.list_collection_names():
            logger.warning(f"Expected collection '{expected_collection_name}' not found in database!")
            
        # Check other databases on this connection
        client = current_db.client
        logger.info("All databases on this MongoDB instance:")
        for db_name in client.list_database_names():
            if db_name not in ['admin', 'config', 'local']:
                db = client[db_name]
                logger.info(f"  - {db_name}:")
                for coll_name in db.list_collection_names():
                    count = db[coll_name].count_documents({})
                    logger.info(f"    - {coll_name}: {count} documents")
        
        logger.info("=== End of Database Consistency Check ===")
        
        return {
            "status": "complete",
            "expected_db": expected_db_name,
            "current_db": current_db_name,
            "expected_collection": expected_collection_name,
            "current_collection": current_collection_name
        }
    except Exception as e:
        logger.error(f"Error in database consistency check: {str(e)}")
        return {
            "status": "error",
            "error": str(e)
        }

@db_connection
def fix_database_consistency(db_recipe):
    """Fix database consistency by copying recipes between collections."""
    try:
        logger.info("Starting database consistency fix operation")
        
        # Get database connection
        db = db_recipe.database
        client = db.client
        
        # Get expected names from environment
        expected_db_name = os.getenv('MONGO_DATABASE', 'recipeDB')
        expected_collection = os.getenv('RECIPE_COLLECTION_NAME', 'recipes')
        
        # Check if we're in the correct database (case-insensitive)
        actual_db_name = db.name
        if actual_db_name.lower() != expected_db_name.lower():
            logger.warning(f"Database name mismatch: actual '{actual_db_name}', expected '{expected_db_name}'")
            # Find database with matching name regardless of case
            db_found = False
            for db_name in client.list_database_names():
                if db_name.lower() == expected_db_name.lower():
                    logger.info(f"Found database with matching name (different case): '{db_name}'")
                    db = client[db_name]
                    db_found = True
                    break
            
            if not db_found:
                logger.info(f"Creating new database: '{expected_db_name}'")
                db = client[expected_db_name]
        
        # Identify source and target collections
        collections = db.list_collection_names()
        source_collections = []
        target_collection = None
        
        # Find potential recipe collections
        for coll_name in collections:
            if coll_name.lower() == expected_collection.lower():
                target_collection = coll_name
            elif coll_name in ['Food', 'recipes']:
                source_collections.append(coll_name)
        
        # If target collection doesn't exist, create it
        if not target_collection:
            logger.info(f"Target collection '{expected_collection}' not found, creating it")
            db.create_collection(expected_collection)
            target_collection = expected_collection
        
        # Get handle to target collection
        target_coll = db[target_collection]
        
        # Count existing recipes in target
        target_count_before = target_coll.count_documents({})
        logger.info(f"Target collection '{target_collection}' has {target_count_before} recipes before sync")
        
        # Copy recipes from source collections to target
        total_copied = 0
        
        for source_name in source_collections:
            if source_name == target_collection:
                continue  # Skip if same as target
                
            source_coll = db[source_name]
            source_count = source_coll.count_documents({})
            
            if source_count > 0:
                logger.info(f"Copying {source_count} recipes from '{source_name}' to '{target_collection}'")
                
                # Find recipes in source that don't exist in target
                recipes_to_copy = []
                for recipe in source_coll.find():
                    recipe_id = recipe['_id']
                    # Check if this recipe already exists in target
                    existing = target_coll.find_one({"_id": recipe_id})
                    if not existing:
                        recipes_to_copy.append(recipe)
                
                if recipes_to_copy:
                    logger.info(f"Found {len(recipes_to_copy)} unique recipes to copy")
                    # Insert recipes one by one to handle any issues
                    copied_count = 0
                    for recipe in recipes_to_copy:
                        try:
                            target_coll.insert_one(recipe)
                            copied_count += 1
                        except Exception as e:
                            logger.error(f"Error copying recipe {recipe.get('_id')}: {str(e)}")
                    
                    logger.info(f"Successfully copied {copied_count} recipes from '{source_name}'")
                    total_copied += copied_count
                else:
                    logger.info(f"No unique recipes to copy from '{source_name}'")
        
        # Count recipes after sync
        target_count_after = target_coll.count_documents({})
        
        return {
            "status": "success",
            "target_collection": target_collection,
            "recipes_before": target_count_before,
            "recipes_copied": total_copied,
            "recipes_after": target_count_after
        }
    except Exception as e:
        logger.error(f"Error fixing database consistency: {str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }

@db_connection
def dump_recipes_as_json(db_recipe, output_dir: str = "recipes") -> int:
    """Dump all recipes as JSON files."""
    try:
        # Ensure the directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        recipes = db_recipe.find({})
        count = 0
        
        for recipe in recipes:
            # Convert ObjectId to string
            recipe_formatted = _format_recipe(recipe)
            
            # Dump the recipe as a JSON file
            file_path = os.path.join(output_dir, f"{recipe_formatted['_id']}.json")
            with open(file_path, 'w') as file:
                json.dump(recipe_formatted, file, indent=4)
            count += 1
            
        logger.info(f"Dumped {count} recipes to {output_dir}")
        return count
    except Exception as e:
        logger.error(f"Error dumping recipes: {str(e)}")
        raise