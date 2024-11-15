
from  hashlib import md5

from .models import Link


def generate_link(longURL):
    hash = encode_to_md5(longURL)
    if hash == None:
        return None
    numberOfCharsInHash = len(hash)
    counter = 0
    while counter < numberOfCharsInHash - 7:
        slug = hash[counter:counter + 7]
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