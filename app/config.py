import os

basedir = os.path.abspath(os.path.dirname(__file__))
WTF_CSRF_ENABLED = True
SECRET_KEY = 'com.tokenoflove.app'
CLOUDINARY_URL = 'cloudinary://959382593352937:UWFmeGPq7IHMYta1PNwHEL1LqrQ@dqwkmzjxu'

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/tol'
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
