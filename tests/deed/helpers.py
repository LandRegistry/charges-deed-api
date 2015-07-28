from random import randint
from app.deed.model import Deed


class DeedHelper:
    _id = randint(1, 999999)
    _json_doc = {
        "provisions": [],
        "borrowers": [
            {
                "id": "1",
                "name": "John Smith",
                "address": {
                    "street-address": "test street",
                    "postal-code": "RG1 1DP",
                    "locality": "London",
                    "extended-address": "test-extended address"
                }
            }
        ],
        "restrictions": [],
        "signatures": [],
        "effective-clause": "const",
        "lender": {
            "name": "Bank Test",
            "address": {
                "street-address": "test street",
                "postal-code": "RG1 1DP",
                "locality": "London",
                "extended-address": "test-extended address"
            },
            "company-number": "1233123ADF"
        },
        "title": {
            "address": {
                "street-address": "test street",
                "postal-code": "RG1 1DP",
                "locality": "London",
                "extended-address": "test-extended address"
            },
            "title-number": "123ABC"
        },
        "charging-clause": "const",
        "mdref": 2
    }

    @staticmethod
    def _create_deed_db():
        DeedHelper._id = randint(1, 999999)

        deed = Deed()
        deed.id = DeedHelper._id

        new_jdoc = DeedHelper._json_doc

        new_jdoc["borrowers"][0]["token"] = Deed.generate_token()

        new_jdoc = {"operative-deed": new_jdoc}

        deed.json_doc = new_jdoc

        deed.save()

        return deed

    @staticmethod
    def _create_deed():
        DeedHelper._id = randint(1, 999999)

        deed = Deed()
        deed.id = DeedHelper._id
        deed.json_doc = DeedHelper._json_doc

        return deed

    @staticmethod
    def _delete_deed(_id):
        Deed.delete(_id)
