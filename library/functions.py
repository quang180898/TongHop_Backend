import binascii
import os
import re
import json
import base64
from PIL import Image
import io

from datetime import date, timedelta, datetime
from cryptography.fernet import Fernet
from django.contrib.postgres.fields import jsonb

from django.db import models
from django.db.models.functions import Cast
from collections import OrderedDict
from rest_framework import exceptions

from math import isnan

from library.constant.services import PASSWORD_ENCODE_KEY


def merge_dicts(dict1, dict2):
    for k in set(dict1.keys()).union(dict2.keys()):
        if k in dict1 and k in dict2:
            if isinstance(dict1[k], dict) and isinstance(dict2[k], dict):
                yield (k, dict(merge_dicts(dict1[k], dict2[k])))
            else:
                yield (k, dict2[k])
        elif k in dict1:
            yield (k, dict1[k])
        else:
            yield (k, dict2[k])


def today():
    return date.today()


def day_add(time, number):
    try:
        return time + timedelta(days=number)
    except (ValueError, TypeError):
        return None


def day_sub(time, number):
    try:
        return time - timedelta(days=number)
    except (ValueError, TypeError):
        return None


def now():
    return datetime.now()


def convert_string_to_day(string, default=None):
    try:
        return datetime.strptime(string, '%Y-%m-%d')
    except (ValueError, TypeError):
        return default


def convert_string_to_bool(string=None, default=False):
    if string:
        if isinstance(string, bool):
            return string
        try:
            string = int(string)
        except:
            pass
        if isinstance(string, int):
            if 1 == string:
                return True
            else:
                return False
        if isinstance(string, str):
            string = string.strip().lower()
            if 'true' == string:
                return True
            else:
                return False
        return default
    else:
        return default


def convert_to_int(string, default=0):
    try:
        return int(string)
    except:
        return default


def convert_string_to_int(string, default=None):
    try:
        return int(string)
    except:
        return default


def convert_string_to_list(string, default=None):
    try:
        project_sale_status = list(json.loads(string.replace("'", '"')))
    except:
        project_sale_status = default
    return project_sale_status


def convert_to_billion(number, decimal=2, default=0):
    print(number)
    try:
        return round(number / 10 ** 9, decimal)
    except:
        return default


def convert_list_to_string(list, default="[]"):
    try:
        listToStr = "[" + ','.join(map(str, [i for i in list if i])) + "]"
        return listToStr
    except:
        return default


def convert_to_bool(boolean_str, default=False):
    try:
        boolean_str = boolean_str.lower().strip()
        if boolean_str == 'true':
            return True
        if boolean_str == 'false':
            return False
    except:
        return default


def convert_to_boolean(boolean_str, default=False):
    try:
        boolean_str = boolean_str.lower().strip()
        if boolean_str == 'true':
            return True
        if boolean_str == 'false':
            return False
    except:
        return None


def convert_to_float(string, default=0.0):
    try:
        return float(string) if not isnan(float(string)) else default
    except:
        return default


def convert_to_dict(string, default={}):
    try:
        return json.loads(string)
    except:
        return default


def end_a_day(_date):
    try:
        to_day = _date.strftime("%d/%m/%Y")
    except AttributeError:
        return None

    _time = datetime.strptime(
        '{} 23:59:59'.format(to_day), '%d/%m/%Y %H:%M:%S')

    return _time


def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + timedelta(days=4)
    return next_month - timedelta(days=next_month.day)


def string_to_time(_string, _format='%d/%m/%Y %H:%M:%S'):
    try:
        return datetime.strptime(_string, _format)
    except (ValueError, IndexError, AttributeError):
        return None


def time_to_string(_time, _format='%d/%m/%Y %H:%M:%S'):
    if _time:
        return _time.strftime(_format)
    return ''


def is_email_valid(email):
    pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'

    regex = re.compile(pattern)

    if email is None or (email is not None and regex.search(email)):
        return True
    else:
        return False


def format_email(email):
    if email:
        email = email.lower()
        email = email.strip()
        return email
    return None


def format_name(name):
    if name:
        return name.strip().lower()
    return None


def format_mobile(mobile):
    if mobile:
        mobile = mobile.strip()
        mobile = mobile.replace('.', '')
        mobile = mobile.replace(',', '')
        mobile = mobile.replace('-', '')
        mobile = mobile.replace(' ', '')
        return mobile
    return None


def is_mobile_valid(mobile):
    pattern = '^(0)+([0-9]{9})$'
    regex = re.compile(pattern)

    if mobile is None or (mobile is not None and regex.search(mobile)):
        return True
    else:
        return False


def is_valid_id_number(id_number):
    pattern = '^([0-9]{9}|[0-9]{12}|(?!^0+$)[a-zA-Z0-9]{3,20})$'
    regex = re.compile(pattern)
    if id_number and regex.search(str(id_number)):
        return True
    else:
        return False


def check_json_load_key_exists(key, json_loads):
    if key in json_loads.keys():
        return json_loads.get(key)
    return None


def get_value_list(list, key):
    try:
        value_list = [obj[key] for obj in list]
        return value_list
    except Exception as e:
        return []


def get_dict_list(object_list, key, value):
    try:
        con = [obj for obj in object_list if obj[key] == value]
        return con
    except:
        return []


def get_value_jsonField(key, column, type=None):
    if type is None:
        type = models.IntegerField()
    return Cast(jsonb.KeyTextTransform(key, column), type)


def search_object_list(object_list, mapping_key, mapping_value_list):
    try:
        result = dict()
        inserted_key = []
        for obj in object_list:
            if obj[mapping_key] not in inserted_key and obj[mapping_key] in mapping_value_list:
                result[obj[mapping_key]] = []
                inserted_key.append(obj[mapping_key])
            if obj[mapping_key] in inserted_key:
                result[obj[mapping_key]].append(obj)

        return result
    except:
        return dict()


def unique_key_in_object_list(object_list, key):
    key_list = []
    result = []
    for obj in object_list:
        if obj[key] not in key_list:
            result.append(obj)
            key_list.append(obj[key])
    return result


def get_character_first(str):
    s = str.split(' ')
    text = ""
    for i in s:
        text += i[0]
    return text


def roman_number(num):
    roman = OrderedDict()
    roman[1000] = "M"
    roman[900] = "CM"
    roman[500] = "D"
    roman[400] = "CD"
    roman[100] = "C"
    roman[90] = "XC"
    roman[50] = "L"
    roman[40] = "XL"
    roman[10] = "X"
    roman[9] = "IX"
    roman[5] = "V"
    roman[4] = "IV"
    roman[1] = "I"

    def roman_num(num):
        num = int(num) if isinstance(num, int) or num.isdigit() else 0
        for r in roman.keys():
            x, y = divmod(num, r)
            yield roman[r] * x
            num -= (r * x)
            if num <= 0:
                break

    return "".join([a for a in roman_num(num)])


def validate_exception(text):
    fail = {
        'success': False,
        'detail': text,

    }
    raise exceptions.ValidationError(fail)


def validate_type_int(**kwargs):
    assert isinstance(kwargs, dict)
    for key, value in kwargs.items():
        if isinstance(value, int):
            try:
                data = int(value)
            except:
                validate_exception("%s type is int" % str(key))
        if isinstance(value, list):
            for temp in value:
                try:
                    data = int(temp)
                except:
                    validate_exception("items in %s type is int" % str(key))


def format_integer(value):
    try:

        _value = int(value) if value else 0

        return ("{:,}".format(_value).replace(',', '.')) if _value != 0 else ''
    except:
        return "N/A"


def convert_character(text):
    patterns = {
        '[àáảãạăắằẵặẳâầấậẫẩ]': 'a',
        '[đ]': 'd',
        '[èéẻẽẹêềếểễệ]': 'e',
        '[ìíỉĩị]': 'i',
        '[òóỏõọôồốổỗộơờớởỡợ]': 'o',
        '[ùúủũụưừứửữự]': 'u',
        '[ỳýỷỹỵ]': 'y'
    }
    output = text
    for regex, replace in patterns.items():
        output = re.sub(regex, replace, output)
        # deal with upper case
        output = re.sub(regex.upper(), replace.upper(), output)
    return output


def sizeof_fmt(num, suffix='B'):
    if num:
        for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
            if abs(num) < 1024.0:
                return "{}{}{}".format(round(num), unit, suffix)
            num /= 1024.0
        return "{}{}".format(num, suffix)
    else:
        return "0KB"


def generate_token(key):
    token = binascii.hexlify(os.urandom(20)).decode()

    key = '{}:{}'.format(key, token)
    key = key.encode()

    try:
        return base64.b64encode(key).decode()
    except:
        return None


def convert_byte_to_base64(byte: bytes = None):
    if not byte:
        return None
    return base64.b64encode(byte).decode('utf-8')


def get_multi_fs_to_byte(list_object):
    try:
        tmp_byte = bytes()
        check_order = 1
        for data_byte in list_object:
            order = data_byte['n']
            if check_order > order:
                tmp_byte += data_byte['data']
                check_order += 1
            else:
                return None
        return tmp_byte
    except:
        return None


def get_thumbnail(base64_byte):
    try:
        image = Image.open(io.BytesIO(base64_byte))
        width, height = image.size
        image.thumbnail((200, (200*width)/height))
        data = io.BytesIO()
        image.save(data, format="PNG", quality=10)
        return base64.b64encode(data.getvalue()).decode('utf-8')
    except:
        return None


def encrypt_password(password):
    fernet = Fernet(PASSWORD_ENCODE_KEY.encode())
    encrypted_password = fernet.encrypt(str(password).encode())
    return encrypted_password.decode()


def decrypt_password(encrypted_password, default=''):
    try:
        fernet = Fernet(PASSWORD_ENCODE_KEY)
        decrypted_password = fernet.decrypt(encrypted_password.encode())
        return decrypted_password.decode()
    except:
        return default


def get_value_list_in_object_list(key, list):
    try:
        value_list = [obj[key] for obj in list]
        return value_list
    except:
        return []
