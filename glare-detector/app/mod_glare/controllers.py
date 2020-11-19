# Import flask dependencies
from flask import Blueprint, request, jsonify

from app.mod_glare.services import Glare

# Define the blueprint: 'glare', set its url prefix: app.url/glare
mod_glare = Blueprint('glare', __name__, url_prefix='/glare')
glare = Glare()

# Set the route and accepted methods
@mod_glare.route('/detect', methods=['POST'])
def detect():
    """
    API that process the metadata requests and determines if there is a
    possibility of direct glare in the associated image or not.
    ---
    requests:
        {
            "lat": a float between 0 to 90 that shows the latitude in which the image was taken
            "lon": a float between -180 to 180 that shows the longitude in which the image was taken
            "epoch": Linux epoch in second
            "orientation": a float between -180 and 180 the east-ward orientation of car travel from
                           true north. 0 means nort. 90 is east and -90 is west.
        }

    responses:
      500:
        { 
            'status': Shows the "error" status.
            'detail': Description of the error.
        }
      200:
        {
            'status': Shows the "success" status.
            "glare": True if glare is present, False otherwise.
        }
    """
    # Store request body as a metadata variable
    metadata = request.get_json()

    # Call detect_glare service function
    res = glare.detect_glare(metadata)
    if res['status'] == "error":
        # Return error if not successful
        return jsonify(res), 500
    return jsonify(res), 200
    
