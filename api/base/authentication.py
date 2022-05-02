from django.db.models import F

from api.base.base_authentication import BaseBasicAuthentication, BaseTokenAuthentication
from django.utils.translation import gettext_lazy as _
from django.utils import translation
from rest_framework import exceptions
from library.functions import now

from library.constant.custom_messages import CUSTOM_ERROR_MESSAGE, INVALID_LOGIN, INACTIVE_USER, INVALID_TOKEN, OTP_INVALID
from library.otp import get_otp
from library.authorization import check_dev_env, login_exception, get_language_header

# from core.postgres.customer.models import Customer


# check token authorize
class TokenAuthentication(BaseTokenAuthentication):
    def authenticate_credentials(self, user_id, token, request=None):
        # self.check_otp_header(request)
        error_code = None
        user = None
        try:
            user = Customer.objects.filter(pk=user_id, active_flag=True).first()
        except:
            error_code = INVALID_LOGIN

        if not user:
            user = None
            error_code = INVALID_LOGIN

        elif token != user.token:
            user = None
            error_code = INVALID_TOKEN

        setattr(request, 'user', user)
        setattr(request, 'error_code', error_code)
        self.authorize_user(request)
        return user, token

    def authenticate_header(self, request):
        return self.keyword

    def authorize_user(self, request):
        lang_code = get_language_header(request)
        user = request.user
        error_code = request.error_code

        if not user:
            fail = login_exception(error_code, lang_code)
            raise exceptions.AuthenticationFailed(fail)

        return None

    def check_otp_header(self, request):
        if not self.check_device_otp_valid(request):
            fail = {
                'success': False,
                'code': OTP_INVALID,
                'detail': CUSTOM_ERROR_MESSAGE[OTP_INVALID]}
            raise exceptions.AuthenticationFailed(fail)
        return None

    def check_device_otp_valid(self, request):
        if request:
            # bypass OTP in dev env.
            if check_dev_env(request):
                pass
            else:
                http_device = request.META.get('HTTP_MNV_DEVICE')

                if not http_device:
                    return False

                otp_cur, otp_pre, otp_next = get_otp()

                try:
                    device_otp = http_device
                except ValueError:
                    return False

                if device_otp not in (otp_cur, otp_pre, otp_next):
                    return False

            return True

        return False


# Login authorize
class BasicAuthentication(BaseBasicAuthentication):

    def authenticate_credentials(self, username, password, request=None):
        credentials = {
            'username': username,
            'password': password
        }
        user, error_code = self.authorize_user(**credentials)
        if error_code:
            lang_code = get_language_header(request)
            fail = login_exception(error_code, lang_code)
            raise exceptions.AuthenticationFailed(fail)
        
        user.last_login = now()
        user.save()
        setattr(request, 'user', user)
        return user, error_code  # authentication successful

    @staticmethod
    def authorize_user(**credentials):
        user = None
        try:
            user = Customer.objects.get(username=credentials['username'], active_flag=True)
            if user.check_password(credentials['password']):
                if user.active_flag and user.email_confirmed_flag:
                    return user, None
                return None, INACTIVE_USER
            else:
                if user:
                    return None, INVALID_LOGIN
                return None, INVALID_LOGIN
        except:
            return None, INVALID_LOGIN
