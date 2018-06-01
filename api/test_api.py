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
        
    
    def test_request_not_exist(self):
        response = self.app.get(BASE_URL+"/5")
        self.assertEqual(response.status_code, 404)
    
    def test_get_requests(self):
        response = self.app.get(BASE_URL+"/2")
        self.assertEqual(response.status_code, 200)

    def test_get_request(self):
        response = self.app.get(BASE_URL+"/2")
        self.assertEqual(response.status_code, 200)

    def test_create_request(self):
        #ensure no missing values
        user_request = {'id': 5,'userID':5,'description':'pc over heats even on low activity'}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(user_request),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)

        #ensure title is string
        user_request = {'id': 5,'userID':5,'title':1,'description':'pc over heats even on low activity'}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(user_request),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)

        #ensure description is string
        user_request = {'id': 5,'userID':5,'description':2}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(user_request),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)

        #ensure no repeated requests
        user_request = {'id': 6,'userID':5,'title': 'pc over heat','description':'pc over heats even on low activity'}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(user_request),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)

        #ensure correct request passes
        user_request = {'id': 6,'userID':5,'title': 'new request','description':'pc over heats even on low activity'}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(user_request),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_modify_request(self):
        #ensure no editing non existing requests
        modify_request = {"title":"New title","description":"New Description"}
        response = self.app.put(BASE_URL+"/7",
                                data=json.dumps(modify_request),
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)
        
        #ensure description or title is not a non string
        modify_request = {"description":1}
        response = self.app.put(BASE_URL+"/2",
                                data=json.dumps(modify_request),
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)

        modify_request = {"title":1}
        response = self.app.put(BASE_URL+"/2",
                                data=json.dumps(modify_request),
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)
        
        #ensure correct request passes
        modify_request = {"description":"New Description"}
        response = self.app.put(BASE_URL+"/2",
                                data=json.dumps(modify_request),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        # reset app.requests to initial state
        apifunctions.user_requests = self.backup_requests


if __name__ == "__main__":
    unittest.main()