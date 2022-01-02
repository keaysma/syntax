from flask_mongoengine import MongoEngine
from mongoengine import CASCADE, DENY, Q

db = MongoEngine()

# Word definition with a lazy approach, slower, but, easier to manage
class FreeWord(db.Document):
    word = db.StringField(
        required = True,
        null = False,
        min_length = 1
    )

    props = db.ListField(db.StringField())

# Word definition class with exhaustive properties
'''
pronoun
noun
verb
verb_transitive
verb_intransitive
verb_ditransitive
adverb
adjective
determiner
preposition
conjunction
interjection

plural
'''

class Word(db.Document):
    word = db.StringField(
        required = True,
        null = False,
        min_length = 1
    )

    pronoun = db.BooleanField(
        required = True,
        null = False,
        default = False
    )

    noun = db.BooleanField(
        required = True,
        null = False,
        default = False
    )