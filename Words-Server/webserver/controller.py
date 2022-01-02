from .words.model import db as word_db, FreeWord

from .wordbuilder import fetchLikelyClass

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
limiter = Limiter(
    key_func=get_remote_address,
    #default_limits=["200 per day", "50 per hour"]
)

def get_word(word):
    res = FreeWord.objects(word = word).fields(
        id = 0, 
        word = 1, 
        props = 1
    ).first()

    if res: return res

    props = fetchLikelyClass(word)

    if not props or len(props) == 0:
        return None

    res = FreeWord(
        word = word,
        props = props
    )

    res.save()

    return {
        'word': word,
        'props': props
    }