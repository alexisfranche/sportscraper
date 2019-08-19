from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderTimedOut


google_locator = GoogleV3(api_key="AIzaSyAglwogS08ArRJ7rUQu7xu_yGJxr6ZanZI")


def geocode_address(address):
    try:
        location = google_locator.geocode(address, exactly_one=True, timeout=5)
    except GeocoderTimedOut as e:
        print("GeocoderTimedOut: geocode failed on input %s with message %s" % (address, e.msg))
    except AttributeError as e:
        print("AttributeError: geocode failed on input %s with message %s" % (address, e.msg))
    if location:
        address_geo = location.address
        latitude = location.latitude
        longitude = location.longitude
        return address_geo, latitude, longitude
    else:
        print("Geocoder couldn't geocode the following address: %s" % address)