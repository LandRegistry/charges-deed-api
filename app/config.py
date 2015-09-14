import os

DEBUG = True

SQLALCHEMY_DATABASE_URI = os.getenv('DEED_DATABASE_URI',
                                    'postgres:///deed_api')

CASE_API_BASE_HOST = os.getenv('CASE_API_ADDRESS',
                               'http://0.0.0.0:7000')
