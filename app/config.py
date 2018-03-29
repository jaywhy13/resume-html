import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    static_url_path = '/static'
    static_folder = 'static'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'my-big-secret'
    TEMPLATES_AUTO_RELOAD = True