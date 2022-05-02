import requests
import json
from django.utils import translation

from library.functions import convert_list_to_string
# from config.root_local import SERVICE_DETECT_KEY, CLOUD_SERVER_URL
from library.constant.services import MNV_ENCODE, CHATTING_SERVICE_KEY
import tensorflow as tf

HEADER = {
    'Content-Type': 'application/json',
    "MNV-ENCODE": MNV_ENCODE,
    # 'Authorization': 'bearer ' + SERVICE_DETECT_KEY
}

CHATTING_SERVICE_HEAR = {
    'Content-Type': 'application/json',
    "MNV-ENCODE": MNV_ENCODE,
    "CHATTING_SERVICE_API_KEY": CHATTING_SERVICE_KEY,
}

# HEADER_SERVICE_CLOUD = {
#     'Content-Type': 'application/json',
#     "MNV-ENCODE": MNV_ENCODE,
#     'Authorization': 'bearer ' + CLOUD_SERVER_KEY
# }


def request_error(description):
    data = {
        "Error": description,
        "success": False
    }
    return data


def request_api(url, method, content={}, params={}, files=None, headers=HEADER, objects=None):
    if 'MNV-LANGUAGE' in headers:
        headers["MNV-LANGUAGE"] = translation.get_language()

    for key in params.keys():
        if isinstance(params[key], list):
            params[key] = convert_list_to_string(params[key])
    try:
        if method.lower() == 'post':
            if files:
                response = requests.post(
                    url, files=files)
                data = response.content
            else:
                response = requests.post(
                    url, params=params, data=json.dumps(content), headers=headers, verify=False)
                data = response.content
            return response.status_code, data
        elif method.lower() == 'put':
            if objects:
                response = requests.put(
                    url, data=objects)
                data = response.content
            else:
                response = requests.put(
                    url, params=params, data=json.dumps(content), headers=headers, verify=False)
                data = response.content
            return response.status_code, data
        elif method.lower() == 'get':
            response = requests.get(
                url, params=params, data=json.dumps(content), headers=headers, verify=False)
            data = response.content
            return response.status_code, data
        elif method.lower() == 'delete':
            response = requests.delete(
                url, params=params, data=content, headers=headers, verify=False)
            data = response.content
            return response.status_code, data

    except requests.exceptions.HTTPError as err:
        data = request_error(f"Http Error: {err}")
    except requests.exceptions.ConnectionError as err:
        data = request_error(f"Error Connecting: {err}")
    except requests.exceptions.Timeout as err:
        data = request_error(f"Timeout Error: {err}")
    except requests.exceptions.RequestException as err:
        data = request_error(f"OOps: Something Else: {err}")

    return data

# API theo tensorflow server
def request_api_tensorflow_plate(imgs,
               model_name='1',
               host='localhost',
               port=8501,
               signature_name="serving_default"):

    imgs = tf.image.decode_image(imgs, channels=3)
    imgs = tf.expand_dims(imgs, 0)
    imgs = tf.image.resize(imgs, (416, 416))
    imgs = imgs / 255

    imgs = imgs.numpy()
    if imgs.ndim == 3:
        imgs = np.expand_dims(imgs, axis=0)

        
    data = json.dumps({
        "signature_name": signature_name,
        "instances": imgs.tolist()
    })
    
    headers = {"content-type": "application/json"}
    json_response = requests.post('http://{}:{}/v1/models/{}:predict'.format(host, port, model_name), data=data, headers=headers)
    print(json_response.text)
    
    if json_response.status_code == 200:
        y_pred = json.loads(json_response.text)['predictions']
        y_pred = np.argmax(y_pred, axis=-1)
        return y_pred
    else:
        return None