from copy import deepcopy
import unittest
import json

import apifunctions

BASE_URL = 'http://127.0.0.1:5000/api/v1/requests'
BAD_ITEM_URL = '{}/5'.format(BASE_URL)
GOOD_ITEM_URL = '{}/3'.format(BASE_URL)


class TestFlaskApi(unittest.TestCase):

    def setUp(self):
        self.app = apifunctions.app.test_client()
        self.backup_requests = deepcopy(apifunctions.requests)  # no references!
        self.app.testing = True

    def test_get_all_requests(self):
        response = self.app.get(BASE_URL)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['requests']), 3)

    def test_get_one_request(self):
        response = self.app.get(BASE_URL)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['requests'][0]['title'], 'laptop screen blacked out')

    def test_request_not_exist(self):
        response = self.app.get(BAD_ITEM_URL)
        self.assertEqual(response.status_code, 404)

    def test_post_request(self):
        # missing value field = bad
        request = {"title": "some_request"}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(request),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        # value field cannot take str
        request = {"title": "screen", "description": 200}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(request),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        # valid: both required fields, value takes string
        request = {"title": "screen", "description": 'string'}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(request),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data())
        self.assertEqual(data['request']['id'], 4)
        self.assertEqual(data['request']['title'], 'screen')
        # cannot add request with same title again
        request = {"title": "screen", "description":'string'}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(request),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_modify_request(self):
        request = {"description":"new description"}
        response = self.app.put(GOOD_ITEM_URL,
                                data=json.dumps(request),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data['request']['description'], "new description")
        # proof need for deepcopy in setUp: update app.items should not affect self.backup_items
        # this fails when you use shallow copy
        self.assertEqual(self.backup_requests[2]['description'], 'pc over heats even on low activity')  # org value

    def test_modify_error(self):
        # cannot edit non-existing item
        request = {"description": 'string does not exist'}
        response = self.app.put(BAD_ITEM_URL,
                                data=json.dumps(request),
                                content_type='application/json')
        self.assertEqual(response.status_code, 404)
        # value field cannot take int
        request = {"description": 30}
        response = self.app.put(GOOD_ITEM_URL,
                                data=json.dumps(request),
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)


    def tearDown(self):
        # reset app.items to initial state
        apifunctions.requests = self.backup_requests


if __name__ == "__main__":
    unittest.main()