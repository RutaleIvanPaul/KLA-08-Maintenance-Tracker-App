from copy import deepcopy
import unittest
import json

import apifunctions

BASE_URL = 'http://127.0.0.1:8085/api/v1/requests'


class TestApi(unittest.TestCase):

    def setUp(self):
        self.app = apifunctions.app.test_client()
        self.backup_requests = deepcopy(apifunctions.user_requests)  # no references!
        self.app.testing = True
    
    def test_get_requests(self):
        response = self.app.get(BASE_URL+"/2")
        self.assertEqual(response.status_code, 200)

    def test_get_request(self):
        response = self.app.get(BASE_URL+"/2")
        self.assertEqual(response.status_code, 200)

    def test_create_request(self):
        #no missing values
        request = {
        'id': 5,
        'userID':5,
        'title': 'pc over heat',
        'description':'pc over heats even on low activity'
    }
        response = self.app.post(BASE_URL,
                                 data=json.dumps(request),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)

    ''' def test_modify_request(self):
        request = {"description":"New Description"}
        response = self.app.put(BASE_URL+"/2",
                                data=json.dumps(request),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200) '''

    def tearDown(self):
        # reset app.requests to initial state
        apifunctions.requests = self.backup_requests


if __name__ == "__main__":
    unittest.main()