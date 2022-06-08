LOCAL_MEDIA_ROOT = 'media/'
LOCAL_STATIC_ROOT = 'webs/static/'

LOCAL_DEBUG = True

LOGGER_PRINT = False

# Deployed server's qualified domain name

# --- Service detect  ---
SERVICE_DETECT_URL = 'http://172.18.210.18:9001/'
SERVICE_DETECT_KEY = 'MTpiZjdlOTcxYTJjZTNmMmM3MjQ1OGE5NTM2OTMwNGZmMzdkOTZjOGM3'

# --- Cloud Server DEV ---
CLOUD_SERVER_URL = 'https://cloudapi.minerva.vn/'
CLOUD_SERVER_PATH = 'cdn/cctv-dev/'
CLOUD_SERVER_ACCESS_KEY = 'cctv-dev'
CLOUD_SERVER_SECRET_KEY = 'SuAGeJDJy6sXSXHc2'


# --- CoreAPI & Chat DEV ---
SERVICE_CORE_URL = 'https://coreapi.minerva.vn/'
SERVICE_CORE_KEY = 'OTowOGQ0MjE5YmU0YTRhZDhhNGVkYWQ0NzZlZjk5NzI0MzZjZDc5Y2E2'
# - End CoreAPI & Chat DEV ---


# Get map style
LAYOUT_SERVICE_URL = "http://images.minerva.vn:9006"
LAYOUT_SERVICE_KEY = "MTo1ZTAwZjNjZGI4NzRlZDNmZmFhZjUzYWI1OTQ2MGRjYTU1ZDU1YThi"

# LOCAL_SERVER_DOMAIN = "https://cctvapp.minerva.vn"

LOCAL_SERVER_DOMAIN = "https://sneaker-god.netlify.app"

LOCAL_ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'sneaker-god.netlify.app']

# Send mail
CCTV_WEB_URL = 'sau nay them de xac nhan qua mail'

# --- Chatting Server ---
CHATTING_SYSTEM_KEY = 'MTfmZkSrfWNRnukGMj1YmZkSrfWNRlUzZGZ2W2WejOTMzOTAoS0fdsj9S43sdf5'

CHATTING_SERVER = 'http://chatting-api.minerva.vn/'

# --- gRPC --- #

TENSORFLOW_SERVING_HOST = '172.18.201.54'
TENSORFLOW_SERVING_PORT = 8501

RABBIT_NOTIFICATION_INFO = {
    'RABBIT_USER': 'admin',
    'RABBIT_PASS': 'admin@123',
    'RABBIT_HOST': 'cctv-mq.minerva.vn',
    'RABBIT_PORT_WSS': 9202,
    'RABBIT_PORT': 9200,
    'RABBIT_VHOT': 'notification',
    'RABBIT_EXCHANGE_TOPIC': 'amq.topic',
}
