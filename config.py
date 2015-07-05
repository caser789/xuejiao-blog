import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('XUEJIAO-BLOG-SECRET-KEY') or "xuejiao's blog"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.environ.get('EMAIL_163_USERNAME') 
    MAIL_PASSWORD = os.environ.get('EMAIL_163_PASSWORD') 
    BLOG_MAIL_SUBJECT_PREFIX = "[XUEJIAO'S BLOG]"
    BLOG_MAIL_SENDER = 'Xue Jiao <m13488699851@163.com>'
    BLOG_ADMIN = os.environ.get('XUEJIAO-BLOG-ADMIN') 
    BLOG_POSTS_PER_PAGE = 20
    BLOG_FOLLOWERS_PER_PAGE = 50
    BLOG_COMMENTS_PER_PAGE = 30
    SQLALCHEMY_RECORD_QUERIES = True
    BLOG_SLOW_DB_QUERY_TIME = 0.5

    @staticmethod
    def init_app(app):
        pass
    

class DevelopmentConfig(Config):
    DEBUT = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

class ProductionConfig(Config):
    SQLALCHMEY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # email errors to the admin
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'EMAIL_163_USERNAME', None) is not None:
            credentials = (cls.EMAIL_163_USERNAME, cls.EMAIL_163_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_POST),
            fromaddr=cls.BLOG_MAIL_SENDER,
            toaddrs=[cls.BLOG_ADMIN],
            subject=cls.BLOG_MAIL_SUBJECT_PREFIX + ' Application Error',
            credentials=credentials,
            secure=secure)
        mail_handler.setlevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
    }
