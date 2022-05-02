import base64
import binascii

from django.utils.translation import gettext_lazy as _

from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework import exceptions, HTTP_HEADER_ENCODING


class BaseTokenAuthentication(BaseAuthentication):
    """
    Simple token based authentication.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Token ".  For example:

        Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a
    """
    keyword = 'Bearer'
    model = None

    def get_model(self):
        if self.model is not None:
            return self.model
        from rest_framework.authtoken.models import Token
        return Token

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)

        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        receive_token = auth[1]

        user_id, token, msg = self.parse_token(receive_token)
        if msg:
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(user_id, token, request)

    def parse_token(self, key):
        try:
            receive_token = base64.b64decode(key)
            receive_token = receive_token.decode()
        except:
            msg = _('Invalid token header. Token string should not contain spaces.')
            return None, None, msg

        try:
            _info_list = receive_token.split(':')

            if len(_info_list) != 2:
                msg = _('Invalid token value. No credentials provided.')
                return None, None, msg

            user_id = _info_list[0]
            token = _info_list[1]

            return user_id, token, None

        except ValueError:
            msg = 'Split error.'

    def authenticate_header(self, request):
        return self.keyword


class BaseBasicAuthentication(BaseAuthentication):
    """
    HTTP Basic authentication against username/password.
    """
    www_authenticate_realm = 'api'

    def authenticate(self, request):
        username = None
        password = None
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != b'basic':
            msg = _('Invalid basic header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)

        if len(auth) == 1:
            msg = _('Invalid basic header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid basic header. Credentials string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            auth_parts = base64.b64decode(auth[1]).decode(HTTP_HEADER_ENCODING).partition(':')
        except (TypeError, UnicodeDecodeError, binascii.Error):
            msg = _('Invalid basic header. Credentials not correctly base64 encoded.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            username, password = auth_parts[0], auth_parts[2]

        except IndexError:
            msg = _('Invalid basic header. Credentials not correctly format.')
            exceptions.AuthenticationFailed(msg)

        if not username or not password:
            msg = _('No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(username, password, request)

    def authenticate_header(self, request):
        return 'Basic realm="%s"' % self.www_authenticate_realm
