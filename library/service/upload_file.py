import binascii
import os

from config.root_local import CLOUD_SERVER_PATH, CLOUD_SERVER_URL, CLOUD_SERVER_ACCESS_KEY, CLOUD_SERVER_SECRET_KEY
from library.constant.file_check import FILE_TYPE_JPG, FILE_TYPE_JPEG, FILE_TYPE_PNG
import requests


def generate_id():
    return binascii.hexlify(os.urandom(10)).decode()


def get_constant_file_type_from_extension(file_extension):
    if not isinstance(file_extension, str):
        return None
    file_extension = file_extension.lower()
    if file_extension == 'png':
        return FILE_TYPE_PNG
    elif file_extension == 'jpeg':
        return FILE_TYPE_JPEG
    elif file_extension == 'jpg':
        return FILE_TYPE_JPG
    else:
        return None


def upload_file(file_url, file_id, file, _name=None, _url=None, _size=None, _content_type=None):
    if file and file_id and file_url:
        if _content_type:
            content_type = _content_type
        else:
            content_type = file.content_type

        if _name and _url:
            file_extension = _url.split('.')[-1]
            file_name = _name
        else:
            file_extension = file.name.split('.')[-1]
            file_name = file.name.split('.')[0]

        if _size:
            file_size = _size
        else:
            file_size = file.size
        server_file_name = f'{generate_id()}{file_id}.{file_extension}'

        server_file_path = f'{CLOUD_SERVER_PATH}{file_url}/{server_file_name}'

        server_url = f'{CLOUD_SERVER_URL}{server_file_path}'

        headers = {
            'content-type': content_type,
            'access-key': CLOUD_SERVER_ACCESS_KEY,
            'secret-key': CLOUD_SERVER_SECRET_KEY,
            'content-length': str(file_size)
        }
        response = requests.put(
            server_url,
            data=file,
            headers=headers,
            verify=False
        )
        if response.status_code == 200:
            return server_file_path, file_size, get_constant_file_type_from_extension(file_extension), file_name

    return None, 0, 0, 0


def delete_file(server_file_path):
    if server_file_path:
        headers = {
            'access-key': CLOUD_SERVER_ACCESS_KEY,
            'secret-key': CLOUD_SERVER_SECRET_KEY
        }

        server_url = f'{CLOUD_SERVER_URL}{server_file_path}'

        try:
            response = requests.delete(
                server_url,
                headers=headers,
                verify=False
            )

            if response.status_code == 200:
                return True

        except:
            return False

    return False