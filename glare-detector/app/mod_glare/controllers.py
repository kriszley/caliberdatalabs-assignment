# Import flask dependencies
from flask import Blueprint, request, jsonify

from app.mod_glare.services import Glare

# Define the blueprint: 'glare', set its url prefix: app.url/glare
mod_glare = Blueprint('glare', __name__, url_prefix='/glare')
glare = Glare()

# Set the route and accepted methods
@mod_glare.route('/detect', methods=['POST'])
def detect():
    metadata = request.get_json()

    result = glare.detect_glare(metadata)
    if result['status'] == "error":
        return jsonify(result)

    res = {
        "glare": result['glare']
    }

    return jsonify(res)
    
    # Limitation??
    
    # Conditions??

    
