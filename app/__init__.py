import os
from flask import Flask
from app import config
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from pycloudinary import Cloudinary

application = Flask(__name__)
application.config.from_object(config)
db = SQLAlchemy(application)
lm = LoginManager()
lm.init_app(application)
lm.login_view = 'login'
cloudinaryDB = Cloudinary(application)

if not application.debug and os.environ.get('HEROKU') is None:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('app/tmp/tol.log', 'a',
                                        1 * 1024 * 1024, 10)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    application.logger.addHandler(file_handler)
    application.logger.setLevel(logging.INFO)
    application.logger.info('Token Of Love local startup')


if os.environ.get('HEROKU') is not None:
    import logging
    stream_handler = logging.StreamHandler()
    application.logger.addHandler(stream_handler)
    application.logger.setLevel(logging.INFO)
    application.logger.info('Token Of Love startup')

from app import views, models
