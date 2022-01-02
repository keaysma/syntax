from os import environ
from dotenv import load_dotenv

from flask import Flask, jsonify

from .apis import api_blueprint
from .user.model import db as user_db
from .words.model import db as word_db

from .util.database import create_database

from .controller import limiter

def create_app():
    load_dotenv()

    create_database(database = environ.get('PSQL_DB'))

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"{environ.get('PSQL_USER')}://{environ.get('PSQL_PASSWD')}:postgres@localhost:5432/{environ.get('PSQL_DB')}"
    user_db.init_app(app)

    app.config['MONGODB_SETTINGS'] = {
        'db': environ.get('MONGO_DB'),
        'host': 'mongodb+srv://{}:{}@cluster0.0samy.mongodb.net/{}?retryWrites=true&w=majority'.format(
            environ.get('MONGO_USER'),
            environ.get('MONGO_PASSWD'),
            environ.get('MONGO_DB')
        )
    }
    word_db.init_app(app)

    limiter.init_app(app)

    app.register_blueprint(api_blueprint)
    
    return app