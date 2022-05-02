from rest_framework import HTTP_HEADER_ENCODING
import json
import zlib
import datetime
from library.functions import time_to_string
from library.constant.custom_messages import CUSTOM_ERROR_MESSAGE, DATA_NOT_FOUND

from library.logs import logger
from library.otp import get_otp
from django.core.serializers.json import DjangoJSONEncoder
from bson.objectid import ObjectId


CONTENT_TYPE_JSON = b'application/json'
CONTENT_TYPE_FROM_DATA = b'multipart/form-data'
CONTENT_TYPE_IMAGE = b'image/png'
CONTENT_TYPE_TEXT = b'text/plain'
CONTENT_TYPE_VIDEO = b'audio/mp4'

IP_SOCKET_LOCAL = '127.0.0.1'

HTTP_MINERVA = ('Mnv#!535',)

KEY_PASS_RESET = 'c9ad-01b9-4d66-bc88-06b4-49aj'


class DjangoOverRideJSONEncoder(DjangoJSONEncoder):
    """
    JSONEncoder subclass that knows how to encode date/time and decimal types.
    """

    def default(self, o):
        # See "Date Time String Format" in the ECMA-262 specification.
        if isinstance(o, datetime.datetime):
            r = time_to_string(o, "%Y-%m-%d %H:%M:%S")
            return r
        elif isinstance(o, ObjectId):
            r = str(o)
            return r
        else:
            return super(DjangoOverRideJSONEncoder, self).default(o)


def get_ios_authorization_header(request):
    """
    Return request's 'Authorization:' header, as a bytestring.

    Hide some test client ickyness where the header can be unicode.
    """
    auth = request.META.get('HTTP_MINERVA', b'')

    if isinstance(auth, str):
        # Work around django test client oddness
        auth = auth.encode(HTTP_HEADER_ENCODING)
    return auth


def get_content_type_header(request):
    """
    Return request's 'Authorization:' header, as a bytestring.

    Hide some test client ickyness where the header can be unicode.
    """
    content = request.META.get('CONTENT_TYPE', b'')

    try:
        content = content.encode(HTTP_HEADER_ENCODING)
    except:
        content = b''

    return content


def check_content_type_json(request):
    content = get_content_type_header(request).split()

    if content and CONTENT_TYPE_JSON in content[0].lower():
        return True

    return False


def check_content_type_text(request):
    content = get_content_type_header(request).split()

    if content and CONTENT_TYPE_TEXT in content[0].lower():
        return True

    return False


def check_content_type_form(request):
    content = get_content_type_header(request).split()

    if content and CONTENT_TYPE_FROM_DATA in content[0].lower():
        return True

    return False


def check_content_type_image(request):
    content = get_content_type_header(request).split()

    if content and CONTENT_TYPE_IMAGE in content[0].lower():
        return True

    return False


def check_content_type_video(request):
    content = get_content_type_header(request).split()

    if content and CONTENT_TYPE_VIDEO in content[0].lower():
        return True

    return False


def check_dev_env(request):
    if request:
        addr = request.META.get('REMOTE_ADDR')

        if addr in (IP_SOCKET_LOCAL,):
            return True

    return False


def login_exception(code, lang_code):
    if code not in CUSTOM_ERROR_MESSAGE:
        code = DATA_NOT_FOUND
    text = CUSTOM_ERROR_MESSAGE[code][lang_code]
    fail = {
        'success': False,
        'code': code,
        'detail': text,
    }
    return fail


def get_language_header(request, default='vi'):
    lang_code = request.META.get('HTTP_MNV_LANGUAGE', default)
    return lang_code


def get_encode_header(request):
    if request:
        client_encode = request.META.get('HTTP_MNV_ENCODE')

        # if MNV_ENCODE_DISABLED == client_encode:
        #     return False

        try:
            client_encode = int(client_encode)
        except (TypeError, ValueError):
            client_encode = 1

        if client_encode == 0:
            return False
    return True


def service_encode_from_json(_dict):
    try:
        data = json.dumps(_dict, cls=DjangoOverRideJSONEncoder)

        data = data.encode('utf-8')

        data = zlib.compress(data)

        return data
    except Exception as ex:
        logger('--- Error Encode ---')
        logger(ex)
        return ''


def service_decode_to_json(_string):
    try:
        data = zlib.decompress(_string)
        data = data.decode('utf-8')
        data = json.loads(data)
        return data
    except:
        return dict()
