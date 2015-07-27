import unittest
from random import randint

from flask.ext.api import status
from flask import json
from app.deed.model import Deed
from tests.helpers import with_client, setUpApp, \
    with_context, setUpDB, tearDownDB
from tests.deed.helpers import DeedHelper


class TestDeedRoutes(unittest.TestCase):
    def setUp(self):
        setUpApp(self)
        setUpDB(self)

    def tearDown(self):
        tearDownDB(self)

    @with_context
    @with_client
    def test_get_route(self, client):
        deed = DeedHelper._create_deed_db()

        response = client.get('/deed/{}'.format(deed.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(str(deed.id) in response.data.decode())

        DeedHelper._delete_deed(deed.id)

    @with_context
    @with_client
    def test_no_get_route(self, client):
        response = client.get('/deed/{}'.format(randint(1, 9999999)))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @with_context
    @with_client
    def test_delete_route(self, client):
        deed = DeedHelper._create_deed_db()

        response = client.get('/deed/{}'.format(deed.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        Deed.delete(deed.id)

        response = client.get('/deed/{}'.format(deed.id))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @with_context
    @with_client
    def test_sign_route(self, client):
        deed = DeedHelper._create_deed_db()

        response = client.get('/deed/{}'.format(deed.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        signature = "@#$%%^&"
        response = client.post('/deed/{}/{}/signature/'
                               .format(deed.id, "1"),
                               data={"signature": signature})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(str(signature) in response.data.decode())

    @with_context
    @with_client
    def test_sign_route_forbidden(self, client):
        deed = DeedHelper._create_deed_db()

        response = client.get('/deed/{}'.format(deed.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        signature = "@#$%%^&"
        response = client.post('/deed/{}/{}/signature/'
                               .format(deed.id, "10"),
                               data={"signature": signature})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @with_context
    @with_client
    def test_create_generates_token(self, client):
        headers = {'content-type': 'application/json'}

        response = client.post('/deed/',
                               data=json.dumps(DeedHelper._json_doc),
                               headers=headers)

        result = json.loads(response.data)

        get_response = client.get('/deed/{}'.format(result['id']))

        self.assertTrue("token" in get_response.data.decode())

        DeedHelper._delete_deed(result['id'])

    @with_context
    @with_client
    def test_get_by_token(self, client):
        deed = DeedHelper._create_deed_db()

        token = deed.json_doc["operative-deed"]["borrowers"][0]["token"]
        response = client.get('/deed/borrower/{}'.format(token))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(str(token) in response.data.decode())

        DeedHelper._delete_deed(deed.id)
