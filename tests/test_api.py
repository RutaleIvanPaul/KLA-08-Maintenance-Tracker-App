from api import app
from flask_testing import TestCase
import json

class TestAPI(TestCase):
    def create_app(self):
        return app

    def setUp(self):
        with self.client:
            response = self.client.post(
                'api/v1/auth/login',
                data=json.dumps({
                    "email":"test@user.com1",
                    "password":"password"
                }),
                content_type='application/json'
            )
            self.user_data = json.loads(response.data.decode('utf8'))
            # print("User:##########")
            # print(self.user_data)
              
            response = self.client.post(
                    'api/v1/auth/login',
                    data=json.dumps({
                        "email":"test@admin.com2",
                        "password":"password"
                    }),
                    content_type='application/json'
                )
            self.admin_data = json.loads(response.data.decode('utf8'))
            # print("Admin:#######")
            # print(self.admin_data)
        
    # def test_signup(self):
    #     with self.client:
    #         response = self.client.post(
    #             'api/v1/auth/signup',
    #             data=json.dumps({
    #                 "email": "test@user.comtest",
    #                 "password": "password",
    #                 "usertype":"admin"
    #             }),
    #             content_type='application/json'
    #         )
    #         self.assertEqual(response.status_code, 200)


    def test_login(self):
        with self.client:
            response = self.client.post(
                'api/v1/auth/login',
                data=json.dumps({
                    "email": "test@user.com3",
                    "password": "password"
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode('utf8'))
            self.assertIsNotNone(data["token"])
            self.assertEqual(response.status_code, 200)

    def test_login_invalid_email(self):
        with self.client:
            response = self.client.post(
                'api/v1/auth/login',
                data=json.dumps({
                    "email": "test@user3",
                    "password": "password"
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode('utf8'))
            self.assertEqual(response.status_code, 400)

    def test_create_request(self):
        with self.client:
            headers = {"x-access-token":self.user_data["token"]}
            response = self.client.post(
                'api/v1/users/requests',
                data=json.dumps({
                    "title": "This new test Request",
                    "description":"This test description"
                    }),
                content_type='application/json',
                headers=headers
            )
            request_data = json.loads(response.data.decode('utf8'))
            self.assertIsNotNone(request_data)
            self.assertEqual(response.status_code, 201)

    def test_create_request_nonstring_title(self):
        with self.client:
            headers = {"x-access-token":self.user_data["token"]}
            response = self.client.post(
                'api/v1/users/requests',
                data=json.dumps({
                    "title": 2,
                    "description":"This test description"
                    }),
                content_type='application/json',
                headers=headers
            )
            request_data = json.loads(response.data.decode('utf8'))
            self.assertIsNotNone(request_data)
            self.assertEqual(response.status_code, 400)

    def test_create_request_nonstring_description(self):
        with self.client:
            headers = {"x-access-token":self.user_data["token"]}
            response = self.client.post(
                'api/v1/users/requests',
                data=json.dumps({
                    "title":"This Title",
                    "description":1
                    }),
                content_type='application/json',
                headers=headers
            )
            request_data = json.loads(response.data.decode('utf8'))
            self.assertIsNotNone(request_data)
            self.assertEqual(response.status_code, 400)

    def test_create_request_missing_title(self):
        with self.client:
            headers = {"x-access-token":self.user_data["token"]}
            response = self.client.post(
                'api/v1/users/requests',
                data=json.dumps({
                    "title":"",
                    "description":"this description"
                    }),
                content_type='application/json',
                headers=headers
            )
            request_data = json.loads(response.data.decode('utf8'))
            self.assertIsNotNone(request_data)
            self.assertEqual(response.status_code, 400)

    def test_create_request_missing_description(self):
        headers = {"x-access-token":self.user_data["token"]}
        response = self.client.post(
                'api/v1/users/requests',
                data=json.dumps({
                    "title":"this title",
                    "description":""
                    }),
                content_type='application/json',
                headers=headers
            )
        request_data = json.loads(response.data.decode('utf8'))
        self.assertIsNotNone(request_data)
        self.assertEqual(response.status_code, 400)

    def test_modify_request(self):
        with self.client:
            headers = {"x-access-token":self.user_data["token"]}
            response = self.client.put(
                'api/v1/users/requests/1',
                data=json.dumps({
                    "description":"New Description"
                    }),
                content_type='application/json',
                headers=headers
            )
            request_data = json.loads(response.data.decode('utf8'))
            self.assertIsNotNone(request_data)
            self.assertEqual(response.status_code, 200)

    def test_get_requests(self):
        with self.client:
            headers = {"x-access-token":self.user_data["token"]}
            response = self.client.get(
                'api/v1/users/requests',
                content_type='application/json',
                headers=headers
            )
            request_data = json.loads(response.data.decode('utf8'))
            self.assertIsNotNone(request_data)
            self.assertEqual(response.status_code, 200)

    def test_get_particular_request(self):
        with self.client:
            headers = {"x-access-token":self.user_data["token"]}
            response = self.client.get(
                'api/v1/users/requests/1',
                content_type='application/json',
                headers=headers
            )
            request_data = json.loads(response.data.decode('utf8'))
            self.assertIsNotNone(request_data)
            self.assertEqual(response.status_code, 200)

    def test_get_all_requests_on_application(self):
        with self.client:
            headers = {"x-access-token":self.admin_data["token"]}
            response = self.client.get(
                'api/v1/requests',
                content_type='application/json',
                headers=headers
            )
            request_data = json.loads(response.data.decode('utf8'))
            self.assertIsNotNone(request_data)
            self.assertEqual(response.status_code, 200)

    def test_request_not_exist(self):
        with self.client:
            headers = {"x-access-token":self.user_data["token"]}
            response = self.client.get(
                'api/v1/users/requests/100',
                content_type='application/json',
                headers=headers
            )
            request_data = json.loads(response.data.decode('utf8'))
            self.assertIsNotNone(request_data)
            self.assertEqual(response.status_code, 404)

    def test_get_request_missing_values(self):
        with self.client:
            headers = {"x-access-token":self.user_data["token"]}
            response = self.client.get(
                'api/v1/users/requests/',
                content_type='application/json',
                headers=headers
            )
            request_data = json.loads(response.data.decode('utf8'))
            self.assertIsNotNone(request_data)
            self.assertEqual(response.status_code, 404)

    # def test_change_request_status_to_approved(self):
    #     with self.client:
    #         headers = {"x-access-token":self.admin_data["token"]}
    #         response = self.client.put(
    #             'api/v1/requests/7/approve',
    #             content_type='application/json',
    #             headers=headers
    #         )
    #         request_data = json.loads(response.data.decode('utf8'))
    #         self.assertIsNotNone(request_data)
    #         self.assertEqual(response.status_code, 200)

    def test_change_request_status_to_disapproved(self):
        with self.client:
            headers = {"x-access-token":self.admin_data["token"]}
            response = self.client.put(
                'api/v1/requests/1/disapprove',
                content_type='application/json',
                headers=headers
            )
            request_data = json.loads(response.data.decode('utf8'))
            self.assertIsNotNone(request_data)
            self.assertEqual(response.status_code, 200)

    def test_change_request_status_to_resolved(self):
        with self.client:
            headers = {"x-access-token":self.admin_data["token"]}
            response = self.client.put(
                'api/v1/requests/2/resolve',
                content_type='application/json',
                headers=headers
            )
            request_data = json.loads(response.data.decode('utf8'))
            self.assertIsNotNone(request_data)
            self.assertEqual(response.status_code, 200)



    # def test_is_title_string(self):
    #     user_request = {'id': 5,'userID':5,'title':1,'description':'pc over heats even on low activity'}
    #     response = self.app.post(BASE_URL,
    #                              data=json.dumps(user_request),
    #                              content_type='application/json')
    #     self.assertEqual(response.status_code, 400)

    # def test_is_desscription_string(self):
    #     user_request = {'id': 5,'userID':5,'description':2}
    #     response = self.app.post(BASE_URL,
    #                              data=json.dumps(user_request),
    #                              content_type='application/json')
    #     self.assertEqual(response.status_code, 400)

    # def test_no_repeated_strings(self):
    #     user_request = {'id': 6,'userID':5,'title': 'pc over heat','description':'pc over heats even on low activity'}
    #     response = self.app.post(BASE_URL,
    #                              data=json.dumps(user_request),
    #                              content_type='application/json')
    #     self.assertEqual(response.status_code, 400)
        

    # def test_modify_request(self):
    #     modify_request = {"description":"New Description"}
    #     response = self.app.put(BASE_URL+"/2",
    #                             data=json.dumps(modify_request),
    #                             content_type='application/json')
    #     self.assertEqual(response.status_code, 200)
    # def test_editing_nonexisting_requests(self):
    #     modify_request = {"title":"New title","description":"New Description"}
    #     response = self.app.put(BASE_URL+"/7",
    #                             data=json.dumps(modify_request),
    #                             content_type='application/json')
    #     self.assertEqual(response.status_code, 400)
        
    # def test_modify_request_description_not_string(self):
    #     modify_request = {"description":1}
    #     response = self.app.put(BASE_URL+"/2",
    #                             data=json.dumps(modify_request),
    #                             content_type='application/json')
    #     self.assertEqual(response.status_code, 400)
    
    # def test_modify_request_title_not_string(self):
    #     modify_request = {"title":1}
    #     response = self.app.put(BASE_URL+"/2",
    #                             data=json.dumps(modify_request),
    #                             content_type='application/json')
    #     self.assertEqual(response.status_code, 400)