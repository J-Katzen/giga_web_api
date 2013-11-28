# -*- coding: utf-8 -*-

from flask import current_app
from bson.objectid import ObjectId
from wsgiref.handlers import format_date_time
from time import mktime
import requests
import json
import hashlib
import base64


def readable_time(datetime):
    stamp = mktime(datetime.timetuple())
    return format_date_time(stamp)


def api_return(status, updated, id, collection):
    data = {'data': {'status': status, 'updated': readable_time(updated),
                     'id': str(id), 'collection': collection}}
    return json.dumps(data)


def created_date(objectid):
    o = ObjectId(objectid)
    return o.generation_time


def generic_update(general_object, data):
    for key, value in data.iteritems():
        setattr(general_object, key, value)
    return general_object


def get_index(seq, attr, value):
    idx = next(
        (index for (index, d) in enumerate(seq) if d[attr] == value), None)
    return idx


def generic_delete(collection_path, id):
    r = requests.get(crud_url + collection_path + id + '/')
    if r.status_code == requests.codes.ok:
        res = r.json()
        d = requests.delete(crud_url + collection_path + id + '/',
                            headers={'If-Match': res['etag']})
        return d
    else:
        err = {'error': 'Could not find element in' +
               collection_path + ' with id ' + id}
        return err


def create_dict_from_form(req_form):
    d = {}
    for key, value in req_form.iteritems():
        if key in ['email', 'uname', 'perma_name', 'firstname', 'lastname']:
            d[key] = value.lower()
        elif key in ['active', 'fb_login', 't_login', 'completed']:
            if value.lower() in ['true', 'yes', 't', '1']:
                d[key] = True
            else:
                d[key] = False
        elif value.isdigit():
            d[key] = int(value)
        else:
            d[key] = value
    return d


def b64_hash_url(email):
    t_sha = hashlib.sha512()
    t_sha.update(email + current_app.config.get('GIGA_VERIFY_HASH_SALT'))
    return base64.urlsafe_b64encode(t_sha.digest())


BASE2 = "01"
BASE10 = "0123456789"
BASE16 = "0123456789abcdef"
BASE62 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz"


def baseconvert(number, fromdigits, todigits):
    """ converts a "number" between two bases of arbitrary digits

    The input number is assumed to be a string of digits from the
    fromdigits string (which is in order of smallest to largest
    digit). The return value is a string of elements from todigits
    (ordered in the same way). The input and output bases are
    determined from the lengths of the digit strings. Negative
    signs are passed through.

    decimal to binary
    >>> baseconvert(555,BASE10,BASE2)
    '1000101011'

    binary to decimal
    >>> baseconvert('1000101011',BASE2,BASE10)
    '555'

    integer interpreted as binary and converted to decimal (!)
    >>> baseconvert(1000101011,BASE2,BASE10)
    '555'

    base10 to base4
    >>> baseconvert(99,BASE10,"0123")
    '1203'

    base4 to base5 (with alphabetic digits)
    >>> baseconvert(1203,"0123","abcde")
    'dee'

    base5, alpha digits back to base 10
    >>> baseconvert('dee',"abcde",BASE10)
    '99'

    decimal to a base that uses A-Z0-9a-z for its digits
    >>> baseconvert(257938572394L,BASE10,BASE62)
    'E78Lxik'

    ..convert back
    >>> baseconvert('E78Lxik',BASE62,BASE10)
    '257938572394'

    binary to a base with words for digits (the function cannot convert this back)
    >>> baseconvert('1101',BASE2,('Zero','One'))
    'OneOneZeroOne'

    """

    if str(number)[0] == '-':
        number = str(number)[1:]
        neg = 1
    else:
        neg = 0

    # make an integer out of the number
    x = 0
    for digit in str(number):
        x = x * len(fromdigits) + fromdigits.index(digit)

    # create the result in base 'len(todigits)'
    if x == 0:
        res = todigits[0]
    else:
        res = ""
        while x > 0:
            digit = x % len(todigits)
            res = todigits[digit] + res
            x = int(x / len(todigits))
        if neg:
            res = "-" + res

    return res
