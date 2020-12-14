class Config:
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://do_it_yourself_r19c:ap@localhost/tilanvaraus'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = 'ap'

    JWT_ERROR_MESSAGE_KEY = 'message'

    JWT_BLACKLIST_ENABLED = True

    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']