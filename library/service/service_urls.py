# from config.root_local import SERVICE_CORE_URL


# SERVICE_SYSTEM_COUNTRIES_ALL_URL = f'{SERVICE_CORE_URL}{VERSION_1_QUERY}/location/countries'
# SERVICE_SYSTEM_REGION_ALL_URL = f'{SERVICE_CORE_URL}{VERSION_1_QUERY}/location/regions'
# SERVICE_SYSTEM_PROVINCE_ALL_URL = f'{SERVICE_CORE_URL}{VERSION_1_QUERY}/location/provinces'
# SERVICE_SYSTEM_DISTRICT_FROM_PROVINCE_URL = f'{SERVICE_CORE_URL}{VERSION_1_QUERY}/location/districts'
# SERVICE_SYSTEM_WARD_FROM_DISTRICT_URL = f'{SERVICE_CORE_URL}{VERSION_1_QUERY}/location/wards'

# SERVICE_SYSTEM_FIND_COUNTRY = f'{SERVICE_CORE_URL}{VERSION_1_QUERY}/location/find/countries'
# SERVICE_SYSTEM_FIND_PROVINCE = f'{SERVICE_CORE_URL}{VERSION_1_QUERY}/location/find/provinces'
# SERVICE_SYSTEM_FIND_DISTRICT = f'{SERVICE_CORE_URL}{VERSION_1_QUERY}/location/find/districts'
# SERVICE_SYSTEM_FIND_WARD = f'{SERVICE_CORE_URL}{VERSION_1_QUERY}/location/find/wards'

# SERVICE_SYSTEM_SEARCH_ALL = f'{SERVICE_CORE_URL}{VERSION_1_SERVICE}/map/search_all'
from config.root_local import LAYOUT_SERVICE_URL, LAYOUT_SERVICE_KEY
from library.constant.services import MNV_ENCODE

SERVICE_VMS_URL = 'api/v1/devices/cameras/'
SERVICE_CHATTING_CREATE_URL = 'chat_api/v1/user/create'
SERVICE_CHATTING_LOGIN_URL = 'chat_api/v1/user/login_chat'
SERVICE_VMS_RECORDING_SETTING = 'api/v1/devices/cameras/recording-schedule?camera_ids='
LAYOUT_UPLOAD_URL = f'{LAYOUT_SERVICE_URL}/upload/image'

LAYOUT_HEADER = {
    'Content-Type': 'application/json',
    "MNV-ENCODE": MNV_ENCODE,
    'Authorization': 'bearer ' + LAYOUT_SERVICE_KEY
}
