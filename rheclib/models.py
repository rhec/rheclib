import logging
import urllib
# requires python 2.6 or simplejson installed
import simplejson

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

class Geolocated(models.Model):
    """
    Contains fields for location in free text, and fields where that location can be normalized into latitude/longitude
    coordinates and a standardized street address.  Depends on having google maps do the geocoding, so have your api
    key set in settings.GOOGLE_MAPS_API
    """
    location = models.TextField(_('location'), null=True, blank=True, help_text="Full address or city/state, or whatever")
    latitude = models.FloatField(_('latitude'), null=True, blank=True)
    longitude = models.FloatField(_('longitude'), null=True, blank=True)
    postal_code = models.CharField(_('postal code'), max_length="255", null=True, blank=True)
    street = models.CharField(_('street address'), max_length="255", null=True, blank=True)
    city = models.CharField(_('city'), max_length="255", null=True, blank=True)
    state = models.CharField(_('state'), max_length="255", null=True, blank=True)
    county = models.CharField(_('county'), max_length="255", null=True, blank=True)
    country = models.CharField(_('country'), max_length="255", null=True, blank=True)
    location_is_normalized = models.BooleanField(_('is_normalized'), editable=False, default=False)
    
    
    class Meta:
        abstract=True
        
    def normalize_address(self, placemark):
        """
        Normalize all address fields.  Expects placemark data in format like that returned by google.
        The wisdom of mapping away from google's intentionally vague names to US-centric terms is questionable.
        """
        address = placemark['AddressDetails']
        try:
            self.country = address['Country']['CountryName']
        except KeyError:
            logging.warning("could not get country from geocoding")
        try:
            self.state = address['Country']['AdministrativeArea']['AdministrativeAreaName']
        except KeyError:
            logging.warning("could not get state from geocoding")
        try:
            self.county = address['Country']['AdministrativeArea']['SubAdministrativeArea']['SubAdministrativeAreaName']
        except KeyError:
            logging.warning("could not get county from geocoding")
        try:
            self.city = address['Country']['AdministrativeArea']['SubAdministrativeArea']['Locality']['LocalityName']
        except KeyError:
            logging.warning("could not get city from geocoding")
        try:
            self.street = address['Country']['AdministrativeArea']['SubAdministrativeArea']['Locality']['Thoroughfare']['ThoroughfareName']
        except KeyError:
            logging.warning("could not get street from geocoding")
        try:
            self.postal_code = address['Country']['AdministrativeArea']['SubAdministrativeArea']['Locality']['PostalCode']['PostalCodeNumber']
        except KeyError:
            logging.warning("could not get postal_code from geocoding")
            
    
    def get_latlng(self):
        """
        If there is a latitude and longitude, return them, otherwise if there is a location, get from google, otherwise, return None
        This is based on a snippet I found somewhere on the web, but can't find again now.  If I find it I'll attribute it here.
        """
        if self.location_is_normalized:
            return (self.latitude, self.longitude)
        elif self.location:
            key = settings.GOOGLE_MAPS_API_KEY
            output = "json"
            location = urllib.quote_plus(self.location)
            request = "http://maps.google.com/maps/geo?q=%s&output=%s&key=%s" % (location, output, key)
            data = simplejson.loads(urllib.urlopen(request).read())
            logging.info("data: %s" % (data,))
            if data['Status']['code'] == 200:
                placemark = data['Placemark'][0] # can return more than one - but we just use the first
                self.longitude  = placemark['Point']['coordinates'][0]
                self.latitude  = placemark['Point']['coordinates'][1]
                self.normalize_address(placemark)
                # make this optional?
                self.location_is_normalized = True
                self.save()
                return (self.latitude, self.longitude)
            else:
                # lookup failed
                logging.error("Error with geocoding request. Return value was: %s" % data)
                return (None, None)
            
        else:
            return (None, None)