import os
class DefaultConfig(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@mysql:3306/gestion_bibliotheque'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    REDIS_URL = "redis://redis:6379/0"
    CACHE_TYPE = 'redis'
    SECRET_KEY = os.urandom(32)
    WTF_CSRF_SECRET_KEY = SECRET_KEY
    # SERVER_NAME = 'localhost:8000'
    WTF_CSRF_ENABLED = False
    Biblio_api_URL = "http://localhost:8082"


class ProductionConfig(DefaultConfig):
    DEBUG = False
    SESSION_COOKIE_DOMAIN = False