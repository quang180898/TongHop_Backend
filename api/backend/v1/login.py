from django.contrib.auth.hashers import check_password

from api.base.apiViews import APIView
from core.postgres.shoes_store.customer.models import Customer
from library.constant.api import (
    SERVICE_CODE_NOT_EXISTS_BODY, SERVICE_CODE_BODY_PARSE_ERROR, SERVICE_CODE_CUSTOMER_ERROR,
    SERVICE_CODE_WRONG_PASSWORD
)
from library.functions import convert_byte_to_base64


class LoginView(APIView):
    def post(self, request):
        if not request.body:
            return self.response_exception(code=SERVICE_CODE_NOT_EXISTS_BODY)
        try:
            content = self.decode_to_json(request.body)
        except Exception as ex:
            return self.response_exception(code=SERVICE_CODE_BODY_PARSE_ERROR, mess=str(ex))
        key_content_list = list(content.keys())
        check_keys_list = ['user_name', 'pass_word']
        user_name = content.get('user_name')
        pass_word = content.get('pass_word')
        if not all(key in key_content_list for key in check_keys_list):
            return self.validate_exception(
                'Missing ' + ", ".join(str(param) for param in check_keys_list if param not in key_content_list))
        customer_login = Customer.objects.filter(
            username=user_name,
            deleted_flag=False
        ).values(
            'id',
            'username',
            'password',
            'name',
            'mail',
            'mobile',
            'address',
            'image_bytes',
            'permission__code',
            'permission__name',
        ).first()
        if customer_login:
            if check_password(pass_word, customer_login['password']) is True:
                return self.response(self.response_success({
                    "customer_id": customer_login['id'],
                    "username": customer_login['username'],
                    "name": customer_login['name'],
                    "mail": customer_login['mail'],
                    "mobile": customer_login['mobile'],
                    "address": customer_login['address'],
                    "image_bytes": convert_byte_to_base64(customer_login['image_bytes']),
                    "permission_code": customer_login['permission__code'],
                    "permission_name": customer_login['permission__name'],
                }))
            return self.response_exception(code=SERVICE_CODE_CUSTOMER_ERROR)
        else:
            return self.response_exception(code=SERVICE_CODE_CUSTOMER_ERROR)
