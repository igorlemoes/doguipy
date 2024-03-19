from hashlib import sha1
from random import random

from playhouse.sqlite_ext import SqliteExtDatabase
from slugify import slugify

from models.models import get_db

################## Password HASH #########################
db = get_db()

def get_hexdigest(salt, raw_password):
    data = salt + raw_password
    return sha1(data.encode('utf8')).hexdigest()

# @db.func()
def make_password(raw_password):
    salt = get_hexdigest(str(random()), str(random()))[:5]
    hsh = get_hexdigest(salt, raw_password)
    return '%s$%s' % (salt, hsh)

# @db.func()
def check_password(raw_password, enc_password):
    salt, hsh = enc_password.split('$', 1)
    return hsh == get_hexdigest(salt, raw_password)
################## Password HASH #########################


def string_to_num_response(text_pass):

    text = text_pass.lower()

    if text in ['01', 'um', 'hum', 'uma', 'one']:
        return '1'
    
    elif text in ['02', 'dois', 'doiz', 'duas', 'two', 'twos']:
        return '2'
    
    elif text in ['03', 'tres', 'três', 'three', 'threes']:
        return '3'
    
    elif text in ['04', 'quatro', 'cuatro', 'four', 'fours']:
        return '4'
    
    elif text in ['05', 'cinco', 'cincos', 'five', 'fives']:
        return '5'
    
    elif text in ['06', 'seis', 'six', 'sixes']:
        return '6'
    
    elif text in ['07', 'sete', 'seven', 'sevens']:
        return '7'
    
    elif text in ['08', 'oito', 'eight', 'eights']:
        return '8'

    elif text in ['09', 'nove', 'nine', 'nines']:
        return '9'
    
    elif text in ['s', 'sin', 'siim', 'yes', 'ss']:
        return 'sim'
    
    elif text in ['n', 'nao', 'not', 'non']:
        return 'não'
    
    else:
        return text_pass


def is_valid_url(url):
    import re
    regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?<!\.)'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return True is not None and regex.search(url)


def slug(e):
    e.sender.value = slugify(e.sender.value)
    e.sender.update()