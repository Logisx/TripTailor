import os

import configparser
import redis
import secrets
from dotenv import load_dotenv
from .routes import setup_routes 

from flask import Flask
from flask_session import Session
from loguru import logger

_ = load_dotenv(override=True)

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


def init(app):
    config = configparser.ConfigParser()
    config_location = "triptailor/etc/defaults.cfg"
    
    # Configure the app settings
    try:
        logger.info("Initializing app")
        if not config.read(config_location):
            raise FileNotFoundError(f"Config file not found at: {config_location}")

        app.config['DEBUG'] = config.getboolean("config", "debug", fallback=False)
        app.config['ip_address'] = config.get("config", "ip_address", fallback="127.0.0.1")
        app.config['port'] = config.getint("config", "port", fallback=5000)
        app.config['url'] = config.get("config", "url", fallback="http://127.0.0.1:5000")
        
        # Redis session storage configuration
        try:
            app.secret_key = os.getenv('FLASK_APP_SECRET_KEY', default='BAD_SECRET_KEY')
            app.config['SESSION_TYPE'] = config.get("config", "session_type", fallback='redis')
            app.config['SESSION_PERMANENT'] = False
            app.config['SESSION_USE_SIGNER'] = True
            app.config['SESSION_REDIS'] = redis.from_url(
                os.getenv('REDIS_URL', config.get("config", "redis_url", fallback="redis://default:oRT8rb2kdojrS7ot8VnqVHRPqbNMlrdk@redis-13198.c16.us-east-1-3.ec2.redns.redis-cloud.com:13198"))
            )
        except:
            logger.error("Redis configuration error")
        logger.info("App successfully initialized")
    
    except Exception as e:
        logger.error(f"Error loading configs from {config_location}: {e}")
        app.config['DEBUG'] = False
        app.config['ip_address'] = "127.0.0.1"
        app.config['port'] = 5000
        app.config['url'] = "http://127.0.0.1:5000"

init(app) 
server_session = Session(app) # Create a session storage
setup_routes(app) # Connect the routes to the app


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",  # Heroku requires 0.0.0.0
        port=int(os.environ.get("PORT", 5000))  # Default to 5000 if PORT is not set
    )