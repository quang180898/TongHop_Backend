import requests
from requests.exceptions import HTTPError
import json

from config.root_local import SERVICE_CORE_KEY, SERVICE_CORE_URL
from library.constant.services import MNV_ENCODE


HEADER = {
    'Content-Type': 'application/json',
    "MNV-ENCODE": MNV_ENCODE,
    'Authorization': 'bearer ' + SERVICE_CORE_KEY
}


def send_post_message(service_path, data, headers=None, raw_parse=False, raw_url=False):
    try:
        if not headers:
            headers = HEADER
        if not raw_url:
            url = SERVICE_CORE_URL + service_path
        else:
            url = service_path
        # Convert to json
        # data['key'] = SECURITY_KEY
        data = json.dumps(data)
        resp = requests.post(url, data=data, headers=headers, verify=False)
        resp.raise_for_status()

    except HTTPError as http_err:
        return {'error': "1", 'message': 'Đã có lỗi xảy ra (No:{})'.format(http_err)}
    except Exception as err:
        return {'error': "2", 'message': 'Đã có lỗi xảy ra (No:{})'.format(err)}
    else:
        if not raw_parse:
            return resp.json()

        return resp.content
