from pysolar.solar import *
import datetime

class Glare:
    def detect_glare(self, metadata):
        try:
            is_valid = self.validate_metadata(metadata)
            if is_valid != True:
                print(str(is_valid))
                raise Exception(str(is_valid))

            is_glare = "false"

            lat = metadata['lat']
            lon = metadata['lon']
            epoch = metadata['epoch']
            orientation = metadata['orientation']

            # Convert UNIX timestamp to UTC datetime
            date = datetime.datetime.fromtimestamp(epoch, tz=datetime.timezone.utc)

            # Compute azimuth for given latitude, longitude, date
            azimuth = get_azimuth(lat, lon, date)

            # If azimuth > 180 degrees, convert to negative
            azimuth = self.to_neg_degree(azimuth)
            
            # Compute altitude for given latitude, longitude, date
            altitude = get_altitude(lat, lon, date)

            # Compute azimuthal difference between the car and the sun
            azimuthal_diff = abs(orientation - azimuth)

            # True if:
            # 1. Azimuthal difference between 'sun' and the 'direction of the car travel' (and hence the direction of forward-facing camera)
            #    is less than 30 degrees
            # 2. Altitude of the sun is less than 45 degrees
            if azimuthal_diff < 30 and 0 < altitude < 45:
                is_glare = "true"
            return { 'status': "success", 'glare': is_glare }
        except Exception as e:
            return { 'status': "error", 'detail': str(e) }
    
    # If azimuth > 180 degrees, convert to negative
    def to_neg_degree(self, degree):
        if degree > 180:
            return degree - 360
        return degree

    # Validate metadata
    def validate_metadata(self, metadata):
        try:
            lat = metadata['lat']
            if not isinstance(lat, float) and not 0 < lat < 90:
                raise Exception("Latitude: " + str(lat) + " is not a float within 0 to 90.")
            lon = metadata['lon']
            if not isinstance(lon, float) and not -180 < lon < 180:
                raise Exception("Longitude: " + str(lon) + " is not a float within -180 to 180.")
            epoch = metadata['epoch']
            if not 0 < epoch:
                raise Exception("Epoch: " + str(epoch) + " is not a float within 0 to 90.")
            orientation = metadata['orientation']
            if not isinstance(orientation, float) and not -180 < orientation < 180:
                raise Exception("Orientation: " + str(orientation) + " is not a float within -180 to 180.")
            return True
        except Exception as e:
            print("HERE")
            return e
