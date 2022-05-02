from otpauth import OtpAuth
from datetime import datetime


def get_time_value():
    current_time = datetime.now()

    str_current_time = current_time.strftime('%d/%m/%Y %H:%M')

    current_second = current_time.second

    current_time_no_second = int(datetime.strptime(str_current_time, '%d/%m/%Y %H:%M').timestamp())

    if current_second < 30:
        current_time_no_second += 29
    else:
        current_time_no_second += 59

    return current_time_no_second


def get_previous_time_value(current_time_no_second):
    previous_time = current_time_no_second - 30

    return previous_time


def get_otp():
    # otp = OTP()

    time_cur = get_time_value()
    otp_cur = generate_otp(time_cur)

    time_previous = time_cur - 30
    otp_pre = generate_otp(time_previous)

    time_next = time_cur + 30
    otp_next = generate_otp(time_next)

    return otp_cur, otp_pre, otp_next


def generate_otp(time):
    auth = OtpAuth('najvj5u2sd5svty')  # a secret string
    token = format(auth.hotp(time), '06')
    return token
