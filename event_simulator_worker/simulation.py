import time
import os
import random
import requests


LOCATION_API_URL = os.environ.get('LOCATION_API_URL')
DRIVING_ANALYTICS_API_URL = os.environ.get('DRIVING_ANALYTICS_API_URL')

DRIVING_ANALYTICS_DICE_RATIO_MAPPING = {
    'speed_limit': 0.05,
    'speed_acceleration': 0.1,
    'hard_break': 0.02
}


def start_trip_simulation(data, log):
    log('simulation started: {}'.format(data))

    operator_name = data['operator_name']
    shuttle_identifier = data['shuttle_identifier']
    polyline = data['polyline']

    list_of_coords = decode_polyline(polyline)
    for coords in list_of_coords:
        location_data = {
            'coords': coords,
            'operator_name': operator_name,
            'shuttle_identifier': shuttle_identifier
        }
        try:
            requests.post(LOCATION_API_URL, json=location_data)
            log('location data sent: {}'.format(location_data))
        except Exception as e:
            log('location data could not be sent: {}'.format(location_data))

        dice_ratio = throw_dice()
        for violation_type, threshold in (
                DRIVING_ANALYTICS_DICE_RATIO_MAPPING.items()):
            if dice_ratio <= threshold:
                driving_analytics_data = {
                    'violation_type': violation_type,
                    'operator_name': operator_name,
                    'shuttle_identifier': shuttle_identifier,
                    'coords': coords
                }
                try:
                    requests.post(
                        DRIVING_ANALYTICS_API_URL, json=driving_analytics_data
                    )
                    log('driving analytics data sent: {}'.format(
                        driving_analytics_data
                    ))
                except Exception as e:
                    log('driving analytics data could not be sent: {}'.format(
                        driving_analytics_data
                    ))

        time.sleep(0.5)

    log('simulation finished.')


def decode_polyline(_polyline_str):
    def _(polyline_str):
        """
            Pass a Google Maps encoded polyline string; returns
            list of lat/lng pairs
        """
        index, lat, lng = 0, 0, 0
        coordinates = []
        changes = {'latitude': 0, 'longitude': 0}

        # Coordinates have variable length when encoded, so just keep
        # track of whether we've hit the end of the string. In each
        # while loop iteration, a single coordinate is decoded.
        while index < len(polyline_str):
            # Gather lat/lon changes, store them in a dictionary
            # to apply them later
            for unit in ['latitude', 'longitude']:
                shift, result = 0, 0

                while True:
                    byte = ord(polyline_str[index]) - 63
                    index += 1
                    result |= (byte & 0x1f) << shift
                    shift += 5
                    if not byte >= 0x20:
                        break

                if (result & 1):
                    changes[unit] = ~(result >> 1)
                else:
                    changes[unit] = (result >> 1)

            lat += changes['latitude']
            lng += changes['longitude']

            coordinates.append('%s,%s' % (lat / 100000.0, lng / 100000.0))

        return coordinates

    try:
        return _(_polyline_str)
    except IndexError:
        # HACK
        _polyline_str = _polyline_str.replace('\\\\', '\\')
        return _(_polyline_str)


def throw_dice():
    return random.uniform(0, 1)
