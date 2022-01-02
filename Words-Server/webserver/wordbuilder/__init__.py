from os import environ
from itertools import chain

from requests import get
from bs4 import BeautifulSoup


def fetchLikelyClass(word : str) -> list:
    res = check_dictionary_api(word)

    if not res:
        res = check_wordsmyth(word)

    if res and len(res) > 0:
        return generate_smart_props(res)

# Fill in missing properties based on retrieved ones
def generate_smart_props(props : list) -> list:
    new_props : set = set(props)

    # Di. Vergs, and T. Verbs should also have the general verbs property
    if new_props.intersection(['transitive verb', 'ditransitive verb']):
        new_props.add('verb')

    return list(new_props)

def check_dictionary_api(word):
    try:
        res = get(f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={environ.get('DICTIONARY_API_KEY')}")

        data : list = res.json()

        return [_['fl'] for _ in data]
    except Exception as e:
        print(f'check_dictionary_api: {str(e)}')
        return None




def check_wordsmyth(word):
    return check_wordsmyth_by_url("https://www.wordsmyth.net/?level=3&ent={}".format(word))

def check_wordsmyth_by_url(url):
    print(url)

    res = get(url)

    soup = BeautifulSoup(res.text, 'html5lib')

    # Make sure this is not a words suggestion page, if it is return None
    spelling_header = soup.find('div', text=lambda t: t and 'Did you mean this word?' in t)
    if spelling_header:
        print('suggestions page, abort')
        return None

    # Fetch Singular Part of Speech element
    pos_headers = list(soup.find_all('a', text='part of speech:'))
    if pos_headers and len(pos_headers) > 0:
        print(f'found {len(pos_headers)} "part of speech" elements')
        parts_of_speech = []
        for pos_header in pos_headers:
            pos_container = pos_header.parent.find_next_sibling('td')
            if pos_container:
                pos_elements = pos_container.find_all('a')
                if pos_elements and len(pos_elements) > 0:
                    parts_of_speech += [_.text for _ in pos_elements]
        
        if len(parts_of_speech) > 0:
            return parts_of_speech

    # This is a page to pick between multiple definitions
    wordlist = soup.findAll("div", {"class": "wordlist"})
    if len(wordlist) == 1 and wordlist[0].table:
        print('multi select')

        ref_links = wordlist[0].table.tbody.findAll("a")
        print(ref_links)

        return list(set(chain(*[check_wordsmyth_by_url(ref['href']) for ref in ref_links])))
    
    # No definition found
    print('couldnt find anything')
    return None