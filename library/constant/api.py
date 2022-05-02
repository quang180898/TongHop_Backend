from django.utils.translation import ugettext_lazy as _

URL_MOBILE_API_v1 = 'api.mobile.v1.'
URL_BACKEND_API = 'api.backend.v1.'

CONTENT_TYPE_JSON = b'application/json'
CONTENT_TYPE_FROM_DATA = b'multipart/form-data'
CONTENT_TYPE_IMAGE = b'image/png'

PAGINATOR_PER_PAGE = 20
SERVICE_CODE_NOTIFICATION_MESSAGE_SUCCESS = "Bạn đã đọc hết tin"

SERVICE_CODE_DEVICE_INVALID = 100  # thiết bị không hợp lệ
SERVICE_CODE_NOT_EXISTS_USER = 101  # không tồn tại User
SERVICE_CODE_WRONG_PASSWORD = 102  # Sai mật khẩu
SERVICE_CODE_WRONG_TOKEN = 103  # Sai token
SERVICE_CODE_USER_IS_LOCKED = 104  # Tài khoản bị Aber khóa
SERVICE_CODE_USER_NOT_ACTIVE = 105  # Tài khoản chưa kích hoạt
SERVICE_CODE_DEVICE_OTP_INVALID = 106  # sai OTP
SERVICE_CODE_CUSTOMER_ERROR = 107  # sai TK và PW

SERVICE_CODE_SEND_EMAIL_FAIL = 199  # gửi mail để reset pass khi người dùng quên mật khẩu thất bại
SERVICE_CODE_NOT_FOUND = 200  # data tìm không thấy
SERVICE_CODE_ERROR = 201  # Dùng chung
SERVICE_CODE_ERROR_SEND_SMS = 202  # số di động không hợp lệ
SERVICE_CODE_BODY_PARSE_ERROR = 203  # parse body từ client
SERVICE_CODE_NOT_EXISTS_BODY = 204  # body client gửi lên không tồn tại
SERVICE_CODE_TOKEN_INVALID = 205  # dùng trong service gọi sms otp của khách hàng
SERVICE_CODE_HEADER_INVALID = 206  # header không chứa thông tin nhận diện
SERVICE_CODE_EMAIL_DUPLICATE = 207  # email đã tồn tại
SERVICE_CODE_EMAIL_INVALID = 208  # email không hợp lệ
SERVICE_CODE_CUSTOMER_NOT_EXIST = 209  # customer không tồn tại
SERVICE_CODE_MOBILE_DUPLICATE = 210  # mobile đã tồn tại
SERVICE_CODE_RECORD_DUPLICATE = 211  # Duplicate record
SERVICE_CODE_RECORD_NOT_VALIDATE = 212  # NOT Validate record
SERVICE_CODE_MOBILE_INVALID = 213  # mobile is invalid
SERVICE_CODE_PASSWORD_MISMATCH = 217  # password is not matched
SERVICE_CODE_PROJECT_NOT_EXIST = 220  # project is not exists
SERVICE_CODE_RESOURCE_NOT_EXIST = 221  # resource is not exists
SERVICE_CODE_RESOURCE_DETAIL_NOT_EXIST = 222  # resource detail is not exists
SERVICE_CODE_NAME_REQUIRED = 223  # name is required
SERVICE_CODE_PASSWORD_INVALID = 226
SERVICE_CODE_CODE_REQUIRED = 227

# ---Shoes_Store---
SERVICE_CODE_FULL_NAME_REQUIRED = 228
SERVICE_CODE_ADDRESS_REQUIRED = 229
SERVICE_CODE_BIRTHDAY_REQUIRED = 231
SERVICE_CODE_GENDER_REQUIRED = 232
SERVICE_CODE_IMAGE_REQUIRED = 233
SERVICE_CODE_FILE_SIZE = 235
SERVICE_CODE_FORMAT_NOT_SUPPORTED = 236
SERVICE_CODE_IMAGE_NAME_REQUIRED = 237
SERVICE_CODE_IMAGE_RECOGNITION = 238
SERVICE_CODE_LABEL_LENGTH = 239
SERVICE_CODE_PLATE_NUMBER_LENGTH = 240
SERVICE_CODE_MOBILE_LENGTH = 241
SERVICE_CODE_USER_NAME_DUPLICATE = 242
SERVICE_CODE_SPAM = 400
SERVICE_CODE_MISSING_PERSON_ID = 243
SERVICE_CODE_ERROR_IMAGE = 244
SERVICE_CODE_USER_PERMISSION = 248
SERVICE_CODE_NOT_DO_EVERYTHING = 249
SERVICE_CODE_NOT_FOUND_DETECT_TYPE = 250
SERVICE_CODE_ADMIN_PERMISSION = 251
SERVICE_CODE_USER_EMAIL_DUPLICATE = 253
SERVICE_CODE_USER_MOBILE_DUPLICATE = 254
SERVICE_CODE_SAME_LEVEL_USER_EDIT = 255
SERVICE_CODE_SAME_LEVEL_USER_DELETE = 256
SERVICE_CODE_FULL_NAME_SPECIAL_CHARACTER = 257
SERVICE_CODE_FULL_NAME_ISSPACE = 258
SERVICE_CODE_ADDRESS_ISSPACE = 259
SERVICE_CODE_MOBILE_ISSPACE = 260
SERVICE_CODE_FULL_NAME_NONE = 262
SERVICE_CODE_ADDRESS_NONE = 263
SERVICE_CODE_MOBILE_NONE = 264
SERVICE_CODE_ADDRESS_SPECIAL_CHARACTER = 265
SERVICE_CODE_MAIL_ISSPACE = 266
SERVICE_CODE_MAIL_SPECIAL_CHARACTER = 267
SERVICE_CODE_MAIL_DUPLICATE = 268
SERVICE_CODE_SHOES_NOT_EXIST = 269
SERVICE_CODE_SHOES_USER_NOT_EXIST = 270
SERVICE_CODE_CATEGORY_NOT_EXIST = 271
SERVICE_CODE_BRAND_NOT_EXIST = 272
SERVICE_CODE_DISCOUNT_NOT_EXIST = 273
SERVICE_CODE_PRODUCT_DISCOUNT_EXIST = 274
# -- Dictionary --
SERVICE_MESSAGE = {
    SERVICE_CODE_DEVICE_INVALID: {
        'en': 'Device invalid',
        'vi': 'Thiết bị không hợp lệ'
    },
    SERVICE_CODE_DEVICE_OTP_INVALID: {
        'en': 'OTP invalid',
        'vi': 'OTP không hợp lệ'
    },
    SERVICE_CODE_NOT_EXISTS_USER: {
        'en': 'Not exists user',
        'vi': 'Tài khoản không tồn tại'
    },
    SERVICE_CODE_WRONG_PASSWORD: {
        'en': 'Wrong password',
        'vi': 'Sai mật khẩu'
    },
    SERVICE_CODE_WRONG_TOKEN: {
        'en': 'Token invalid',
        'vi': 'Token không hợp lệ'
    },
    SERVICE_CODE_USER_NOT_ACTIVE: {
        'en': 'Account not active, please contact Admin',
        'vi': 'Tài khoản chưa kích hoạt. Vui lòng liên hệ Admin'
    },
    SERVICE_CODE_USER_IS_LOCKED: {
        'en': 'Your customer blocked, please contact Admin',
        'vi': 'Tài khoản của bạn bị khóa. Vui lòng liên hệ Admin'
    },
    SERVICE_CODE_NOT_FOUND: {
        'en': 'Data not found',
        'vi': 'Không tồn tại dữ liệu'
    },
    SERVICE_CODE_SPAM: {
        'en': 'Spam',
        'vi': 'Spam'
    },
    SERVICE_CODE_HEADER_INVALID: {
        'en': 'Header invalid',
        'vi': 'Header không hợp lệ'
    },
    SERVICE_CODE_BODY_PARSE_ERROR: {
        'en': 'Body parse error',
        'vi': 'Body parse lỗi'
    },
    SERVICE_CODE_NOT_EXISTS_BODY: {
        'en': 'Not exists body',
        'vi': 'Không tìm thấy dữ liệu'
    },
    SERVICE_CODE_EMAIL_DUPLICATE: {
        'en': 'Email duplicate.',
        'vi': 'Email này đã tồn tại trong hệ thống'
    },
    SERVICE_CODE_EMAIL_INVALID: {
        'en': "Email invalid",
        'vi': "Email không hợp lệ"
    },
    SERVICE_CODE_CUSTOMER_NOT_EXIST: {
        'en': "Customer not exists",
        'vi': "Người dùng không tồn tại trong hệ thống"
    },
    SERVICE_CODE_MOBILE_DUPLICATE: {
        'en': "Mobile duplicate",
        'vi': "Số điện thoại đã tồn tại trong hệ thống"
    },
    SERVICE_CODE_RECORD_DUPLICATE: {
        'en': "Record duplicate",
        'vi': "Record đã tồn tại trong hệ thống"
    },
    SERVICE_CODE_RECORD_NOT_VALIDATE: {
        'en': "Data invalid",
        'vi': "Dữ liệu không hợp lệ"
    },
    SERVICE_CODE_MOBILE_INVALID: {
        'en': 'Mobile invalid',
        'vi': "Số điện thoại không hợp lệ"
    },
    SERVICE_CODE_PASSWORD_MISMATCH: {
        'en': "Password mismatch",
        'vi': "Mật khẩu không trùng khớp"
    },
    SERVICE_CODE_RESOURCE_NOT_EXIST: {
        'en': "Resource not exists",
        'vi': "Resource không tồn tại"
    },
    SERVICE_CODE_RESOURCE_DETAIL_NOT_EXIST: {
        'en': 'Polygon not exists',
        'vi': 'Polygon không tồn tại'
    },
    SERVICE_CODE_NAME_REQUIRED: {
        'en': 'Name is required',
        'vi': 'Tên không được để trống'
    },
    SERVICE_CODE_PASSWORD_INVALID: {
        'en': 'Password invalid',
        'vi': 'Mật khẩu không hơp lệ'
    },
    SERVICE_CODE_CODE_REQUIRED:  {
        'en': 'Code is required',
        'vi': 'Code không được để trống'
    },
    SERVICE_CODE_FULL_NAME_REQUIRED: {
        'en': 'Full name is required',
        'vi': 'Họ tên không được để trống'
    },
    SERVICE_CODE_BIRTHDAY_REQUIRED: {
        'en': 'Birthday is required',
        'vi': 'Ngày sinh không được để trống'
    },
    SERVICE_CODE_GENDER_REQUIRED: {
        'en': 'Gender is required',
        'vi': 'Giới tính không được để trống'
    },
    SERVICE_CODE_ADDRESS_REQUIRED: {
        'en': 'Address is required',
        'vi': 'Địa chỉ không được để trống'
    },
    SERVICE_CODE_IMAGE_REQUIRED: {
        'en': 'Image is required',
        'vi': 'Hình ảnh không được để trống'
    },

    SERVICE_CODE_FILE_SIZE: {
        'en': 'File size must be less than 2.5MB',
        'vi': 'Tệp không được lớn hơn 2.5MB'
    },
    SERVICE_CODE_FORMAT_NOT_SUPPORTED: {
        'en': 'Format file not support',
        'vi': 'Định dạng file không hỗ trợ'
    },
    SERVICE_CODE_IMAGE_NAME_REQUIRED:  {
        'en': 'Image name is required',
        'vi': 'Tên hình ảnh không được để trống'
    },
    SERVICE_CODE_IMAGE_RECOGNITION: {
        'en': 'Face identification error',
        'vi': 'Không nhận diện được gương mặt'
    },
    SERVICE_CODE_LABEL_LENGTH: {
        'en': 'Label maximum 12 character',
        'vi': 'Label tối đa 12 ký tự'
    },
    SERVICE_CODE_PLATE_NUMBER_LENGTH: {
        'en': 'Plate number maximum 15 character',
        'vi': 'Biển số tối đa 15 ký tự'
    },
    SERVICE_CODE_MOBILE_LENGTH: {
        'en': 'Mobile must have 10 number, dont have character and space',
        'vi': 'Số điện thoại có 10 số, không chứa khoảng trắng và ký tự'
    },
    SERVICE_CODE_USER_NAME_DUPLICATE: {
        'en': 'Username exists',
        'vi': 'Tên đăng nhập đã tồn tại trong hệ thống'
    },
    SERVICE_CODE_MISSING_PERSON_ID: {
        'en': 'Person id is required',
        'vi': 'Person id không được để trống'
    },
    SERVICE_CODE_ERROR_IMAGE: {
        'en': 'Image invalid',
        'vi': 'Hình ảnh không hợp lệ'
    },
    SERVICE_CODE_USER_PERMISSION: {
        'en': 'User cant do that',
        'vi': 'Người dùng không được quyền thực hiện'
    },
    SERVICE_CODE_NOT_DO_EVERYTHING: {
        'en': 'Not do everything',
        'vi': 'Không có thao tác'
    },
    SERVICE_CODE_NOT_FOUND_DETECT_TYPE: {
        'en': 'Detect type not found',
        'vi': 'Detect type không tồn tại'
    },
    SERVICE_CODE_ADMIN_PERMISSION: {
        'en': 'Only Admin can do that',
        'vi': 'Chỉ admin được thực hiện thao tác này'
    },

    SERVICE_CODE_USER_EMAIL_DUPLICATE: {
        'en': 'Email exist',
        'vi': 'Email đã tồn tại trong hệ thống'
    },
    SERVICE_CODE_USER_MOBILE_DUPLICATE: {
        'en': 'Mobile exist',
        'vi': 'Số điện thoại đã tồn tại trong hệ thống'
    },
    SERVICE_CODE_SAME_LEVEL_USER_EDIT: {
        'en': 'Cant edit same level user',
        'vi': 'Không thể sửa thông tin người dùng cùng bậc'
    },
    SERVICE_CODE_SAME_LEVEL_USER_DELETE: {
        'en': 'Cant delete same level user',
        'vi': 'Không thể xóa người dùng cùng bậc'
    },
    SERVICE_CODE_FULL_NAME_SPECIAL_CHARACTER: {
        'en': 'Full name cannot contain special characters',
        'vi': 'Họ tên không thể chứa ký tự đặc biệt'
    },
    SERVICE_CODE_FULL_NAME_ISSPACE: {
        'en': 'Full name must have characters',
        'vi': 'Họ tên phải có ký tự'
    },
    SERVICE_CODE_ADDRESS_ISSPACE: {
        'en': 'Address must have characters',
        'vi': 'Địa chỉ phải có ký tự'
    },
    SERVICE_CODE_MOBILE_ISSPACE: {
        'en': 'Mobile must have characters',
        'vi': 'SĐT phải có ký tự'
    },
    SERVICE_CODE_FULL_NAME_NONE: {
        'en': 'Full name cant none',
        'vi': 'Họ tên không được để trống'
    },
    SERVICE_CODE_ADDRESS_NONE: {
        'en': 'Address cant none',
        'vi': 'Địa chỉ không được để trống'
    },
    SERVICE_CODE_MOBILE_NONE: {
        'en': 'Mobile cant none',
        'vi': 'SĐT không được để trống'
    },
    SERVICE_CODE_ADDRESS_SPECIAL_CHARACTER: {
        'en': 'Address cannot contain special characters',
        'vi': 'Địa chỉ không thể chứa ký tự đặc biệt'
    },
    SERVICE_CODE_CUSTOMER_ERROR: {
        'en': 'User_name or pass_word error!',
        'vi': 'Sai tài khoản hoặc mật khẩu!'
    },
    SERVICE_CODE_MAIL_ISSPACE: {
        'en': 'Mail must have characters',
        'vi': 'Mail phải có ký tự'
    },
    SERVICE_CODE_MAIL_SPECIAL_CHARACTER: {
        'en': 'Mail cannot contain special characters',
        'vi': 'Mail không thể chứa ký tự đặc biệt'
    },
    SERVICE_CODE_MAIL_DUPLICATE: {
        'en': "Mail duplicate",
        'vi': "Mail đã tồn tại trong hệ thống"
    },
    SERVICE_CODE_SHOES_NOT_EXIST: {
        'en': "Shoes not exists!",
        'vi': "Giày không tồn tại trong hệ thống!"
    },
    SERVICE_CODE_SHOES_USER_NOT_EXIST: {
        'en': "Shoes_user not exists!",
        'vi': "Đơn hàng mua giày không tồn tại trong hệ thống!"
    },
    SERVICE_CODE_CATEGORY_NOT_EXIST: {
        'en': "Category not exists!",
        'vi': "Thể loại sách không tồn tại trong hệ thống!"
    },
    SERVICE_CODE_BRAND_NOT_EXIST: {
        'en': "Brand not exists!",
        'vi': "Thương hiệu không tồn tại trong hệ thống!"
    },
    SERVICE_CODE_DISCOUNT_NOT_EXIST: {
        'en': "Disount not exists!",
        'vi': "Khuyến mãi không tồn tại trong hệ thống!"
    },
    SERVICE_CODE_PRODUCT_DISCOUNT_EXIST: {
        'en': "Product Discount exist!",
        'vi': "Sản phẩm hiện đang có khuyến mãi khác!"
    }
}

# --- Sort method ---

ORDER_BY_ASC = 1
ORDER_BY_DESC = 2

SORT_TYPE = {
    ORDER_BY_ASC: _('asc'),
    ORDER_BY_DESC: _('desc'),
}

SORT_TYPE_CHOICE = ((k, v) for k, v in SORT_TYPE.items())
SORT_TYPE_LIST = [(k, v) for k, v in SORT_TYPE.items()]

SORT_TYPE_TO_ID = {
    'asc': ORDER_BY_ASC,
    'desc': ORDER_BY_DESC
}

GENDER_TYPE_MALE = 1
GENDER_TYPE_FEMALE = 2

GENDER_TYPE = {
    GENDER_TYPE_MALE: _('Nam'),
    GENDER_TYPE_FEMALE: _('Nữ'),
}

GENDER_TYPE_CHOICE = ((k, v) for k, v in GENDER_TYPE.items())
GENDER_TYPE_LIST = [(k, v) for k, v in GENDER_TYPE.items()]

GENDER_TO_ID = {
    'Nam': GENDER_TYPE_MALE,
    'Nữ': GENDER_TYPE_FEMALE
}

ID_TO_GENDER = {
    GENDER_TYPE_MALE: 'Nam',
    GENDER_TYPE_FEMALE: 'Nữ'
}

CAMERA_NOT_RECORD = 1
CAMERA_MOTION_ONLY = 2
CAMERA_ALWAYS_RECORD = 3

CAMERA_RECORDING_TYPE = {
    CAMERA_NOT_RECORD: _('No record'),
    CAMERA_MOTION_ONLY: _('Motion only'),
    CAMERA_ALWAYS_RECORD: _('Record always')
}

CAMERA_RECORDING_CHOICE = ((k, v) for k, v in CAMERA_RECORDING_TYPE.items())
CAMERA_RECORDING_LIST = ((k, v) for k, v in CAMERA_RECORDING_TYPE.items())

ADMIN = 1
MANAGER = 2
USER = 3

USER_PERMISSION = {
    ADMIN: _('Admin'),
    MANAGER: _('Manager'),
    USER: _('User')
}

USER_PERMISSION_ROLE = {
    ADMIN: USER_PERMISSION[ADMIN],
    MANAGER: USER_PERMISSION[MANAGER],
    USER: USER_PERMISSION[USER]
}
USER_PERMISSION_CHOICE = ((k, v) for k, v in USER_PERMISSION_ROLE.items())
USER_PERMISSION_LIST = ((k, v) for k, v in USER_PERMISSION_ROLE.items())

