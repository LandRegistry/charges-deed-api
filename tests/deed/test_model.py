from app.deed.model import Deed
import unittest
from tests.helpers import setUpApp, with_context, setUpDB, tearDownDB
from tests.deed.helpers import DeedHelper


class TestDeedModel (unittest.TestCase):

    def setUp(self):
        setUpApp(self)
        setUpDB(self)

    def tearDown(self):
        tearDownDB(self)

    @with_context
    def test_get(self):
        base_deed = DeedHelper._create_deed_db()
        deed = Deed.get(base_deed.id)

        self.assertEqual(deed.id, base_deed.id)

        DeedHelper._delete_deed(base_deed.id)

    @with_context
    def test_get_deed_by_token(self):
        base_deed = DeedHelper._create_deed_db()

        base_deed_token = \
            base_deed.json_doc["operative-deed"]["borrowers"][0]["token"]

        retrieved_deed_from_token = Deed.get_deed_by_token(base_deed_token)

        self.assertEqual(base_deed.id,
                         retrieved_deed_from_token.id)
        self.assertEqual(base_deed.json_doc,
                         retrieved_deed_from_token.json_doc)

        DeedHelper._delete_deed(base_deed.id)

    @with_context
    def test_delete(self):
        base_deed = DeedHelper._create_deed_db()
        deed = Deed.get(base_deed.id)

        self.assertEqual(deed.id, DeedHelper._id)

        Deed.delete(deed.id)
        deed = Deed.get(deed.id)

        self.assertIs(deed, None)
