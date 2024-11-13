
from dotenv import load_dotenv
from  hashlib import md5
import os

from .models import Link

load_dotenv()
SHORT_URL_CHAR_SIZE = int(os.getenv("SHORT_URL_CHAR_SIZE"))


def generate_link(longURL):
    hash = encode_to_md5(longURL)
    if hash == None:
        return None
    numberOfCharsInHash = len(hash)
    counter = 0
    while counter < numberOfCharsInHash - SHORT_URL_CHAR_SIZE:
        slug = hash[counter:counter + SHORT_URL_CHAR_SIZE]
        link = Link.objects.filter(slug = slug)
        if not link:
            return slug
        counter += 1

def encode_to_md5(longURL):
    try:
        encoder = md5()
        encoder.update(longURL.encode('utf-8'))
        hash = encoder.hexdigest()
        return hash
    except:
        return None