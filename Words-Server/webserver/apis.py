from os import environ

from flask import Blueprint, jsonify, request, current_app

from .user.model import db as user_db, User
from .words.model import db as word_db, FreeWord

from .controller import limiter, get_word

api_blueprint = Blueprint('apis', __name__)

@api_blueprint.route('/word/<word>', methods = ["GET", "POST"])
@limiter.limit(environ.get("API_WORD_FETCH_LIMIT", "25 per hour"))
def word_view(word):
    if request.method == 'POST':
        data = request.json()

        props = data.get('props')

        if not props:
            return jsonify({
                'error': 'missing field "props"'
            }), 400

        w = FreeWord(
            word=word,
            props=props
        )
        w.save()

        return jsonify({
            'word': word
        }), 200

    if request.method == 'GET':
        res = get_word(word)

        if res:
            return jsonify(res), 200

        return jsonify({
            'error': f'could not find word "{word}"'
        }), 404

    return jsonify({
        'error': 'method not allowed'
    }), 405

@api_blueprint.route('/user', methods = ["POST"])
def user():

    db.create_all()

    u = User(username = 'test')

    user_db.session.add(u)
    user_db.session.commit()

    return jsonify({
        'message': 'hello!'
    }), 200