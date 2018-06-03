from copy import deepcopy
import unittest
import json

from api import apifunctions

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
        user_request = {'id': 6,'userID':5,'title': 'new request','description':'pc over heats even on low activity'}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(user_request),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_missing_values(self):
        user_request = {'id': 5,'userID':5,'description':'pc over heats even on low activity'}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(user_request),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_is_title_string(self):
        user_request = {'id': 5,'userID':5,'title':1,'description':'pc over heats even on low activity'}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(user_request),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_is_desscription_string(self):
        user_request = {'id': 5,'userID':5,'description':2}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(user_request),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_no_repeated_strings(self):
        user_request = {'id': 6,'userID':5,'title': 'pc over heat','description':'pc over heats even on low activity'}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(user_request),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        

    def test_modify_request(self):
        modify_request = {"description":"New Description"}
        response = self.app.put(BASE_URL+"/2",
                                data=json.dumps(modify_request),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
    def test_editing_nonexisting_requests(self):
        modify_request = {"title":"New title","description":"New Description"}
        response = self.app.put(BASE_URL+"/7",
                                data=json.dumps(modify_request),
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)
        
    def test_modify_request_description_not_string(self):
        modify_request = {"description":1}
        response = self.app.put(BASE_URL+"/2",
                                data=json.dumps(modify_request),
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    def test_modify_request_title_not_string(self):
        modify_request = {"title":1}
        response = self.app.put(BASE_URL+"/2",
                                data=json.dumps(modify_request),
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)
        
        

    def tearDown(self):
        # reset app.requests to initial state
        apifunctions.user_requests = self.backup_requests


if __name__ == "__main__":
    unittest.main()