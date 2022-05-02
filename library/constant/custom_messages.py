PERMISSION_DENIED = 'PERMISSION_DENIED'
INVALID_LOGIN = 'INVALID_LOGIN'
INVALID_TOKEN = 'INVALID_TOKEN'
USER_NOT_FOUND = 'USER_NOT_FOUND'
DATA_NOT_FOUND = 'DATA_NOT_FOUND'
INACTIVE_USER = 'INACTIVE_USER'
ACTIVATED_USER = 'ACTIVATED_USER'
EXPIRED_TOKEN = 'EXPIRED_TOKEN'
OTP_INVALID = 'OTP_INVALID'
INVALID_DATA = 'INVALID_DATA'
SAME_PASSWORD = 'SAME_PASSWORD'
WRONG_PASSWORD = 'WRONG_PASSWORD'
NEW_PASSWORD_EMPTY = 'NEW_PASSWORD_EMPTY'
INVALID_REPEAT_PASSWORD = 'INVALID_REPEAT_PASSWORD'
USER_NAME_ERROR = 'USER_NAME_ERROR'
USER_NAME_LENGTH = 'USER_NAME_LENGTH'
PASSWORD_LENGTH = 'PASSWORD_LENGTH'

CUSTOM_ERROR_MESSAGE = {
    INVALID_DATA: {
        'vi': 'Dữ liệu không hợp lệ',
        'en': 'Data invalid',
    },
    PERMISSION_DENIED: {
        'vi': 'Bạn không có quyền truy cập',
        'en': 'Permission denied',
    },
    INVALID_LOGIN: {
        'vi': 'Tên đăng nhập hoặc mật khẩu không hợp lệ!',
        'en': 'Invalid username or password',
    },
    USER_NOT_FOUND: {
        'vi': 'Không tồn tại tài khoản',
        'en': 'User does not exist',
    },
    INVALID_TOKEN: {
        'vi': 'Token không hợp lệ',
        'en': 'Invalid token',
    },
    DATA_NOT_FOUND: {
        'vi': 'Không tìm thấy dữ liệu',
        'en': 'Data not found',
    },
    INACTIVE_USER: {
        'vi': 'Tài khoản chưa kích hoạt',
        'en': 'Account is inactive',
    },
    ACTIVATED_USER: {
        'vi': 'Tài khoản đã được kích hoạt',
        'en': 'Account is activated',
    },
    EXPIRED_TOKEN: {
        'vi': 'Token quá hạn',
        'en': 'Token is expired',
    },
    OTP_INVALID: {
        'vi': 'OTP không hợp lệ',
        'en': 'OTP invalid',
    },
    SAME_PASSWORD: {
        'vi': 'Mật khẩu mới trùng với mật khẩu cũ',
        'en': 'New password and current password are the same',
        'zh-hans': 'New password and current password are the same',
    },
    WRONG_PASSWORD: {
        'vi': 'Mật khẩu hiện tại không chính xác',
        'en': 'Current password is wrong',
        'zh-hans': 'Current password is wrong',
    },
    INVALID_REPEAT_PASSWORD: {
        'vi': 'Nhập lại mật khẩu mới không chính xác',
        'en': 'New password and the repeat one are not the same',
        'zh-hans': 'New password and the repeat one are not the same',
    },
    NEW_PASSWORD_EMPTY: {
        'vi': 'Mật khẩu mới không hợp lệ',
        'en': 'New password Invalid',
        'zh-hans': 'New password Invalid',
    },
    USER_NAME_ERROR: {
        'vi': 'Tên đăng nhập không hợp lệ, tên đăng nhập không được có khoảng trắng',
        'en': 'Username Invalid ',
        'zh-hans': 'Username Invalid',
    },
    USER_NAME_LENGTH: {
        'vi': 'Tên đăng nhập có nhiều nhất 25 ký tự và ít nhất 8 ký tự',
        'en': 'Username is at most 25 characters and at least 4 characters',
        'zh-hans': 'Username is at most 25 characters and at least 4 characters',
    },
    PASSWORD_LENGTH: {
        'vi': 'Mật khẩu có nhiều nhất 25 ký tự và ít nhất 8 ký tự',
        'en': 'Password is at most 25 characters and at least 4 characters',
        'zh-hans': 'Password is at most 25 characters and at least 4 characters',
    }
}
