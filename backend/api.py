from flask import Flask, request, jsonify, make_response
from server import (
    addRecipe, getRecipe, updateRecipe, deleteRecipe, 
    searchRecipe, getRecipes, DatabaseError,
    check_db_consistency, fix_database_consistency
)
import json
import logging
import os
from flask_cors import CORS
from functools import wraps
import traceback
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
log_level = os.getenv('LOG_LEVEL', 'info').upper()
log_file = os.getenv('LOG_FILE_PATH', 'api.log')
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

# Initialize Flask app
app = Flask(__name__)

# Configure CORS properly for production
allowed_origins = os.getenv('CORS_ALLOWED_ORIGINS', '*')
if allowed_origins != '*':
    # Parse comma-separated origins into a list
    origins = [origin.strip() for origin in allowed_origins.split(',')]
    logger.info(f"Configuring CORS with specific origins: {origins}")
    CORS(app, 
         resources={r"/api/*": {"origins": origins}},
         supports_credentials=True,
         allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         max_age=86400)  # Cache preflight response for 24 hours
else:
    logger.warning("CORS configured with wildcard origin '*'. This is not recommended for production.")
    CORS(app, 
         resources={r"/api/*": {"origins": "*"}},
         supports_credentials=True,
         allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         max_age=86400)  # Cache preflight response for 24 hours

# Request logging middleware
@app.before_request
def log_request_info():
    logger.info(f"Request: {request.method} {request.path} from {request.remote_addr}")
    if request.method in ['POST', 'PUT'] and request.is_json:
        logger.debug(f"Request payload: {request.json}")

# Error handling decorator
def handle_exceptions(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except DatabaseError as e:
            logger.error(f"Database error: {str(e)}")
            return jsonify({"error": "Database error", "message": str(e)}), 500
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            logger.error(traceback.format_exc())
            return jsonify({"error": "Server error", "message": "An unexpected error occurred"}), 500
    return decorated_function

# API Routes
@app.route('/api/<id>', methods=['PUT'])
@handle_exceptions
def apiPUT(id):
    data = request.json
    if not data:
        return jsonify({"error": "Bad request", "message": "No input data provided"}), 400
    
    response = updateRecipe(id, data)
    return jsonify(response), 200

@app.route('/api/search', methods=['POST'])
@handle_exceptions
def apiSearch():
    data = request.json
    if not data:
        return jsonify({"error": "Bad request", "message": "No search criteria provided"}), 400
    
    recipes = searchRecipe(data)
    return jsonify(recipes), 200

@app.route('/api/search/<search_str>', methods=['GET'])
@handle_exceptions
def apiSearchGet(search_str):
    try:
        search_dict = json.loads(search_str)
        recipes = searchRecipe(search_dict)
        return jsonify(recipes), 200
    except json.JSONDecodeError:
        return jsonify({"error": "Bad request", "message": "Invalid JSON in search parameter"}), 400

@app.route('/api/<id>', methods=['DELETE'])
@handle_exceptions
def apiDELETE(id):
    response = deleteRecipe(id)
    return jsonify(response), 200 if response.get("deleted", False) else 404

@app.route('/api/recipe', methods=['POST'])
@app.route('/api/newRecipe', methods=['POST'])  # Keep the original endpoint for backward compatibility
@handle_exceptions
def apiPOST():
    logger.info('Processing new recipe submission')
    data = request.json
    
    if not data:
        return jsonify({"error": "Bad request", "message": "No input data provided"}), 400
    
    # Basic validation
    required_fields = ['title', 'ingredients']
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        return jsonify({
            "error": "Validation error", 
            "message": f"Missing required fields: {', '.join(missing_fields)}"
        }), 400
    
    recipe_id = addRecipe(data)
    return jsonify({"message": "Recipe added successfully", "recipe_id": recipe_id}), 201

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring and load balancers."""
    try:
        # We could add more complex health checks here if needed
        return jsonify({
            "status": "healthy",
            "service": "recipe-api"
        }), 200
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            "status": "unhealthy",
            "message": str(e)
        }), 500

# Add this route BEFORE the general ID route to prevent conflict
@app.route('/api/db-health', methods=['GET'])
@handle_exceptions
def db_health_check():
    """Check database health and configuration."""
    try:
        # Run the database consistency check
        result = check_db_consistency()
        
        return jsonify({
            "status": "healthy",
            "db_check": result
        }), 200
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        return jsonify({
            "status": "unhealthy",
            "message": str(e)
        }), 500

@app.route('/api/db-fix', methods=['POST'])
@handle_exceptions
def fix_database():
    """Fix database consistency by copying recipes between collections."""
    try:
        result = fix_database_consistency()
        
        return jsonify({
            "status": "success",
            "result": result
        }), 200
    except Exception as e:
        logger.error(f"Database fix operation failed: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
        
@app.route('/api/<id>', methods=['GET'])
@handle_exceptions
def apiGET(id):
    """Get a recipe by ID."""
    # Skip invalid IDs early to avoid wasting resources
    if len(id) != 24 or not all(c in '0123456789abcdefABCDEF' for c in id):
        logger.warning(f"Invalid ObjectId format: {id}")
        return jsonify({
            "error": "Invalid ID format",
            "message": f"The ID {id} is not in a valid format"
        }), 400
    
    logger.info(f"GET request received for recipe ID: {id}")
    
    try:
        recipe = getRecipe(id)
        
        if recipe:
            logger.info(f"Recipe found, returning 200 OK")
            return jsonify(recipe), 200
        else:
            logger.warning(f"Recipe with ID {id} not found")
            return jsonify({
                "error": "Not found", 
                "message": f"Recipe with ID {id} not found"
            }), 404
    except Exception as e:
        logger.error(f"Error in GET /{id}: {str(e)}")
        
        # Check if the error is related to ObjectId conversion
        if "ObjectId" in str(e) and "not a valid ObjectId" in str(e):
            return jsonify({
                "error": "Invalid ID format",
                "message": f"The ID {id} is not in a valid format"
            }), 400
        else:
            return jsonify({
                "error": "Server error", 
                "message": f"Error retrieving recipe: {str(e)}"
            }), 500
    
@app.route('/api/recipes', methods=['GET'])
@app.route('/api/', methods=['GET'])  # Keep the original endpoint for backward compatibility
@handle_exceptions
def getAllRecipes():
    recipes = getRecipes()
    return jsonify(recipes), 200

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found", "message": "The requested URL was not found"}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Method not allowed", "message": "The method is not allowed for the requested URL"}), 405

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Server error", "message": "An internal server error occurred"}), 500

# Consistent response format
@app.after_request
def add_header(response):
    # Ensure JSON content type for all API responses
    response.headers['Content-Type'] = 'application/json'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    
    # Add additional security headers
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    # Log response for debugging
    logger.debug(f"Response: {response.status_code} {response.status}")
    
    return response

# Handle CORS preflight requests  
@app.route('/api/<path:path>', methods=['OPTIONS'])
def handle_preflight(path):
    response = make_response()
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,X-Requested-With')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Max-Age', '86400')
    return response