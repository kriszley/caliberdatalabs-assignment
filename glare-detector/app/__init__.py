# Import flask and template operators
from flask import Flask

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Import a module / component using its blueprint handler variable (mod_glare)
from app.mod_glare.controllers import mod_glare as glare_module

# Register blueprint(s)
app.register_blueprint(glare_module)