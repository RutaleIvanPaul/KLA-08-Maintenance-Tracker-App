import unittest
import flaskapi
import requests
import json
import apifunctions

class TestApi(unittest.TestCase):

     def setUp(self):
        """Define test variables and initialize app."""
        self.app.testing = True
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.request = {'Request Title':'Request Description'}

    def test_createRequest(self):
        """Test whether the API function enables user to create a request"""
        res = self.client().post('/m-tracker/', data=self.request)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Request Description', str(res.data))
    
    def test_getRequest(self):
        """Test whether the API fucntion enables user to get a given request"""
        rv = self.client().post('/m-tracker/', data=self.request)
        self.assertEqual(rv.status_code, 201)
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/m-tracker/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Request Description', str(result.data))

    def test_getRequests(self):
        """Test whether the API function enables user to get requests for all logged in users"""
		res = self.client().post('/m-tracker/', data=self.request)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/m-tracker/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Request Description', str(res.data))

    def test_modifyRequest(self):
        """Test whether the API function enables user to modify given request"""
		rv = self.client().post(
            '/m-tracker/',
            data={'Request Title': 'Request Description'})
        self.assertEqual(rv.status_code, 201)
        rv = self.client().put(
            '/m-tracker/1',
            data={
                'Request Title': 'New Request Description Again'"
            })
        self.assertEqual(rv.status_code, 200)
        results = self.client().get('/m-tracker/1')
        self.assertIn('New Request Description Again', str(results.data))

    
if __name__ == "__main__":
    unittest.main()


