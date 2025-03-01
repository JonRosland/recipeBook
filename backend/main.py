import os
import logging
from gunicorn.app.base import BaseApplication
from api import app
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
log_level = os.getenv('LOG_LEVEL', 'info').upper()
log_file = os.getenv('LOG_FILE_PATH', 'application.log')
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

class StandaloneApplication(BaseApplication):
    """Gunicorn application for WSGI server."""
    
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        for key, value in self.options.items():
            if key in self.cfg.settings and value is not None:
                self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

if __name__ == "__main__":
    # Get configuration from environment variables
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', '6088'))
    workers = int(os.getenv('WORKERS', '3'))  # Default to CPU count * 2 + 1 in production
    log_level = os.getenv('LOG_LEVEL', 'info')
    
    # For development mode
    if os.getenv('FLASK_ENV') == 'development':
        logger.info("Starting in development mode")
        app.run(debug=True, port=port, host=host)
    else:
        # For production mode with Gunicorn
        logger.info(f"Starting in production mode with {workers} workers using gevent")
        options = {
            'bind': f'{host}:{port}',
            'workers': workers,
            'worker_class': 'gevent',  # Using gevent for better async performance
            'timeout': 120,
            'loglevel': log_level,
            'accesslog': '-',  # Log to stdout
            'errorlog': '-',   # Log to stderr
            'reload': False,
            'preload_app': True,
            'keepalive': 65  # Keep connections alive for 65 seconds
        }
        
        StandaloneApplication(app, options).run()