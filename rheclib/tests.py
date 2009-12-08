import logging

from django.test import TestCase
from django.contrib.auth.models import User

from rheclib.models import *

class TestModel(Geolocated):
    pass

class GeolocatedTests(TestCase):
    
    def setUp(self):
        self.test_model = TestModel.objects.create(location="1600 Amphitheatre Pkwy, Mountain View, CA 94043, USA")
        self.test_model.get_latlng()
        
    def tearDown(self):
        pass
        
    def test_get_lat_lng_set_correctly(self):
        self.assertAlmostEqual(self.test_model.latitude, 37.421759)
        self.assertAlmostEqual(self.test_model.longitude, -122.08437)
        
    def test_normalized_address_set_correctly(self):
        self.assertEqual(self.test_model.street, '1600 Amphitheatre Pkwy')
        self.assertEqual(self.test_model.city, 'Mountain View')
        self.assertEqual(self.test_model.state, 'CA')
        self.assertEqual(self.test_model.postal_code, '94043')
        self.assertEqual(self.test_model.county, 'Santa Clara')
        self.assertEqual(self.test_model.country, 'USA')
        
    def test_location_is_normalized_flag_set_correctly(self):
        self.assertTrue(self.test_model.location_is_normalized)
        