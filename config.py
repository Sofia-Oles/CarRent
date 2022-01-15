class Configuration(object):
    SECRET_KEY = "secret_key",
    WTF_CSRF_SECRET_KEY = "a csrf secret key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
