from pysolar.solar import *
import datetime

class Glare:
    def detect_glare(self, metadata):
        """ Given the metadata, determines whether there is a possible glare.
        Args:
            metadata (json): The metadata JSON object:
            Example.
                    {
                        "lat": 49.2699648,
                        "lon": -123.1290368,
                        "epoch": 1588704959.321,
                        "orientation": -10.2
                    }

        Returns:
            dict: The return dict object that contains 
                `status` and `glare` values if successful, and `status` and `details` otherwise.
        """
        try:
            # Validate input metadata
            is_valid = self.validate_metadata(metadata)
            if is_valid != True:
                raise Exception(str(is_valid))

            # Glare set to False by default
            is_glare = "false"

            # Assign metadata into variables
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
    
    def to_neg_degree(self, degree):
        """ Converts the given positive angle degree (>180) into negative value.
        Args:
            degree (float): Positive angle degree value

        Returns:
            degree (float): Converted negative angle degree value
        """
        if degree > 180:
            return degree - 360
        return degree

    # Validate metadata
    def validate_metadata(self, metadata):
        """ Validate whether all of metadata meet the conditions.
        Args:
            metadata (json): The metadata JSON object:
            Example.
                    {
                        "lat": 49.2699648,
                        "lon": -123.1290368,
                        "epoch": 1588704959.321,
                        "orientation": -10.2
                    }

        Returns:
            bool: `True` if pass all the conditions.
            e: Exception object if fail one of the conditions.
        """
        try:
            lat = metadata['lat']
            if not isinstance(lat, float) or not 0 < lat < 90:
                raise Exception("Latitude: " + str(lat) + " is not a float within 0 to 90.")
            lon = metadata['lon']
            if not isinstance(lon, float) or not -180 < lon < 180:
                raise Exception("Longitude: " + str(lon) + " is not a float within -180 to 180.")
            epoch = metadata['epoch']
            if not 0 < epoch:
                raise Exception("Epoch: " + str(epoch) + " is not a float within 0 to 90.")
            orientation = metadata['orientation']
            if not isinstance(orientation, float) or not -180 < orientation < 180:
                raise Exception("Orientation: " + str(orientation) + " is not a float within -180 to 180.")
            return True
        except Exception as e:
            return e
