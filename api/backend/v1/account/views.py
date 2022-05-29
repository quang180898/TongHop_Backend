import re

from django.contrib.auth.hashers import make_password, check_password
from django.db.models import F
from django.core.mail import send_mail
from api.base.apiViews import APIView
from config.settings import DATA_UPLOAD_MAX_MEMORY_SIZE, EMAIL_HOST_USER
from core.postgres.shoes_store.customer.models import Customer
from core.postgres.shoes_store.customer.models import Customer_shoes
from core.postgres.shoes_store.permission.models import Permission
from library.constant.api import (
    SERVICE_CODE_BODY_PARSE_ERROR,
    SERVICE_CODE_NOT_EXISTS_BODY,
    SERVICE_CODE_USER_NAME_DUPLICATE,
    SERVICE_CODE_NOT_FOUND,
    SERVICE_CODE_CUSTOMER_NOT_EXIST,
    SERVICE_CODE_NOT_EXISTS_USER,
    ADMIN,
    SERVICE_CODE_FILE_SIZE,
    SERVICE_CODE_FORMAT_NOT_SUPPORTED,
    SERVICE_CODE_FULL_NAME_SPECIAL_CHARACTER,
    SERVICE_CODE_FULL_NAME_ISSPACE,
    SERVICE_CODE_MAIL_SPECIAL_CHARACTER,
    SERVICE_CODE_MAIL_ISSPACE,
    SERVICE_CODE_MOBILE_ISSPACE,
    SERVICE_CODE_MOBILE_LENGTH,
    SERVICE_CODE_MOBILE_DUPLICATE,
    SERVICE_CODE_MAIL_DUPLICATE,
    USER,
)
from library.constant.custom_messages import (
    INVALID_REPEAT_PASSWORD,
    NEW_PASSWORD_EMPTY,
    PASSWORD_LENGTH,
    USER_NAME_ERROR,
    USER_NAME_LENGTH,
    WRONG_PASSWORD,
    SAME_PASSWORD
)
from library.functions import convert_to_bool, convert_to_int, is_mobile_valid, convert_byte_to_base64
from library.service.upload_file import get_constant_file_type_from_extension


class Account(APIView):
    def list_user(self, request):
        name = self.request.query_params.get('name')
        active_flag = self.request.query_params.get('active_flag')
        user_list = Customer.objects.filter(
            deleted_flag=False
        )
        if name:
            user_list = user_list.filter(name__icontains=name)
        if active_flag:
            user_list = user_list.filter(active_flag=active_flag)

        user_list = user_list.annotate(
            permission_code=F('permission__code'),
            permission_name=F('permission__name')
        ).values(
            'id',
            'name',
            'mobile',
            'username',
            'mail',
            'active_flag',
            'permission_code',
            'permission_name'
        ).order_by('id')
        return self.response(self.response_success(list(user_list)))

    def info_user(self, request):
        user_id = convert_to_int(self.request.query_params.get('user_id'))
        customer = Customer.objects.filter(
            id=user_id,
            deleted_flag=False,
            active_flag=True
        ).annotate(
            permission_code=F('permission__code'),
            permission_name=F('permission__name')
        ).values(
            'id',
            'name',
            'mobile',
            'username',
            'mail',
            'image_bytes',
            'permission_code',
            'permission_name',
            'active_flag'
        ).first()
        if customer:
            customer['image_bytes'] = convert_byte_to_base64(customer['image_bytes'])
            return self.response(self.response_success(customer))
        else:
            return self.response_exception(code=SERVICE_CODE_NOT_FOUND)

    def register(self, request):
        if not request.data:
            return self.response_exception(code=SERVICE_CODE_NOT_EXISTS_BODY)
        try:
            content = request.POST
        except Exception as ex:
            return self.response_exception(code=SERVICE_CODE_BODY_PARSE_ERROR, mess=str(ex))
        if content == {}:
            return self.response_exception(code=SERVICE_CODE_BODY_PARSE_ERROR)
        key_content_list = list(content.keys())
        check_keys_list = ['user_name', 'pass_word', 'password_repeat', 'name', 'mail', 'mobile']

        name = content['name'] if content.get('name') else None
        mobile = content['mobile'] if content.get('mobile') else None
        mail = content['mail'] if content.get('mail') else None
        # user_permission_type = convert_to_int(content['user_permission_type'] if content.get('user_permission_type') else None)
        user_name = content['user_name'] if content.get('user_name') else None
        pass_word = content['pass_word'] if content.get('pass_word') else None
        password_repeat = content['password_repeat'] if content.get('password_repeat') else None
        image = request.FILES['image'] if request.FILES.get('image') else None
        image_name = content.get('image_name')
        if not all(key in key_content_list for key in check_keys_list):
            return self.validate_exception(
                'Missing ' + ", ".join(str(param) for param in check_keys_list if param not in key_content_list))
        if Customer.objects.filter(username=user_name, deleted_flag=False).exists():
            return self.response_exception(code=SERVICE_CODE_USER_NAME_DUPLICATE)
        if user_name is None or ' ' in user_name:
            self.validate_exception(code=USER_NAME_ERROR)
        if len(user_name) < 4 or len(user_name) > 50:
            self.validate_exception(code=USER_NAME_LENGTH)
        if pass_word is None or ' ' in pass_word:
            self.validate_exception(code=NEW_PASSWORD_EMPTY)
        if len(pass_word) < 8 or len(pass_word) > 25:
            self.validate_exception(code=PASSWORD_LENGTH)
        if pass_word != password_repeat:
            self.validate_exception(code=INVALID_REPEAT_PASSWORD)
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        if name is not None:
            if regex.search(name) is not None:
                return self.response_exception(code=SERVICE_CODE_FULL_NAME_SPECIAL_CHARACTER)
            if name.isspace():
                return self.response_exception(code=SERVICE_CODE_FULL_NAME_ISSPACE)
        else:
            return self.validate_exception("Tên không được để trống!")
        if mail is not None:
            if ' ' in mail:
                return self.validate_exception("Mail không được chứa khoảng trắng!")
            if Customer.objects.filter(mail=mail, deleted_flag=False).exists():
                return self.response_exception(code=SERVICE_CODE_MAIL_DUPLICATE)
            if mail.isspace():
                return self.response_exception(code=SERVICE_CODE_MAIL_ISSPACE)
        else:
            return self.validate_exception("Mail không được để trống!")
        if mobile:
            if mobile.isspace():
                return self.response_exception(code=SERVICE_CODE_MOBILE_ISSPACE)
            if is_mobile_valid(mobile) is False:
                return self.response_exception(code=SERVICE_CODE_MOBILE_LENGTH)
            if Customer.objects.filter(mobile=mobile, deleted_flag=False).exists():
                return self.response_exception(code=SERVICE_CODE_MOBILE_DUPLICATE)
        if image:
            if image_name is None:
                return self.validate_exception("missing image_name!")

            img = image_name.split('.')[-1]
            image_name = get_constant_file_type_from_extension(img)
            if image_name is None:
                return self.response_exception(code=SERVICE_CODE_FORMAT_NOT_SUPPORTED)
            size = request.headers['content-length']
            if int(size) > DATA_UPLOAD_MAX_MEMORY_SIZE:
                return self.response_exception(code=SERVICE_CODE_FILE_SIZE)
        user_new = Customer.objects.create(
            name=name,
            username=user_name,
            password=make_password(pass_word),
            mobile=mobile,
            mail=mail,
            permission_id=USER,
            image_bytes=image.read()
        )
        permission = Permission.objects.filter(
            code=user_new.permission_id
        ).values(
            'code',
            'name'
        ).first()

        subject = "HOÀN TẤT ĐĂNG KÝ"
        message = f'Cảm ơn {name} đã đăng ký tài khoản tại website của chúng tôi!'
        mail = send_mail(
            subject=subject,
            message=message,
            from_email=EMAIL_HOST_USER,
            recipient_list=[mail]
        )
        return self.response(self.response_success({
            "user_id": user_new.id,
            "name": user_new.name,
            "mobile": user_new.mobile,
            "email": user_new.mail,
            "user_name": user_new.username,
            "image_base64": user_new.get_image,
            "permission_code": permission['code'],
            "permission_name": permission['name']
        }))

    def update_profile(self, request):
        if not request.data:
            return self.response_exception(code=SERVICE_CODE_NOT_EXISTS_BODY)
        try:
            content = request.POST
        except Exception as ex:
            return self.response_exception(code=SERVICE_CODE_BODY_PARSE_ERROR, mess=str(ex))
        if content == {}:
            return self.response_exception(code=SERVICE_CODE_BODY_PARSE_ERROR)
        user_id = convert_to_int(content.get("user_id"))
        name = content.get("name")
        # mail = content.get("mail")
        mobile = content.get("mobile")
        address = content.get("address")
        image = request.FILES['image'] if request.FILES.get('image') else None
        image_name = content.get('image_name')
        if image:
            if image_name is None:
                return self.validate_exception("missing image_name!")

            img = image_name.split('.')[-1]
            image_name = get_constant_file_type_from_extension(img)
            if image_name is None:
                return self.response_exception(code=SERVICE_CODE_FORMAT_NOT_SUPPORTED)

            size = request.headers['content-length']
            if int(size) > DATA_UPLOAD_MAX_MEMORY_SIZE:
                return self.response_exception(code=SERVICE_CODE_FILE_SIZE)
        if user_id:
            try:
                customer = Customer.objects.get(id=user_id, deleted_flag=False)
            except Customer.DoesNotExist:
                return self.response_exception(code=SERVICE_CODE_CUSTOMER_NOT_EXIST)
            customer.name = name if name is not None else customer.name
            # customer.mail = mail if mail is not None else customer.mail
            customer.mobile = mobile if mobile is not None else customer.mobile
            customer.address = address if address is not None else customer.address
            if image:
                customer.image_bytes = image.read()
            customer.save()
            return self.response(self.response_success({
                "customer_id": customer.id,
                "customer_name": customer.name,
                "customer_mobile": customer.mobile,
                "customer_address": customer.address,
                "customer_mail": customer.mail,
                "customer_image_base64": customer.get_image,
            }))
        else:
            return self.validate_exception("Missing user_id!")

    def change_password(self, request):
        if not request.body:
            return self.response_exception(code=SERVICE_CODE_NOT_EXISTS_BODY)
        try:
            data = self.decode_to_json(request.body)
        except:
            return self.response_exception(code=SERVICE_CODE_BODY_PARSE_ERROR)

        key_content_list = list(data.keys())
        check_keys_list = ['new_password_repeat', 'new_password', 'current_password']
        user_id = convert_to_int(data.get('user_id'))
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        new_password_repeat = data.get('new_password_repeat')
        if 'user_id' in key_content_list:
            if not all(key in key_content_list for key in check_keys_list):
                return self.validate_exception(
                    'Missing ' + ", ".join(str(param) for param in check_keys_list if param not in key_content_list))
            user = Customer.objects.filter(
                id=user_id,
                deleted_flag=False
            ).first()
            if user:
                if check_password(current_password, user.password) is False:
                    self.validate_exception(code=WRONG_PASSWORD)

                if ' ' in new_password:
                    self.validate_exception(code=NEW_PASSWORD_EMPTY)

                if new_password == current_password:
                    self.validate_exception(code=SAME_PASSWORD)

                if len(new_password) < 8 or len(new_password) > 25:
                    self.validate_exception(code=PASSWORD_LENGTH)

                if new_password != new_password_repeat:
                    self.validate_exception(code=INVALID_REPEAT_PASSWORD)
                user.password = make_password(new_password)
                user.save()
                return self.response(self.response_success("Change password success!"))
            else:
                return self.response_exception(code=SERVICE_CODE_CUSTOMER_NOT_EXIST)
        else:
            return self.validate_exception("Missing user_id!")

    def update_active(self, request):
        if not request.body:
            return self.response_exception(code=SERVICE_CODE_NOT_EXISTS_BODY)
        try:
            content = self.decode_to_json(request.body)
        except Exception as ex:
            return self.response_exception(code=SERVICE_CODE_BODY_PARSE_ERROR, mess=str(ex))
        account_id = content.get('account_id')
        active_flag = convert_to_bool(content.get('active_flag'))
        try:
            change_active = Customer.objects.get(id=account_id, deleted_flag=False)
        except Customer.DoesNotExist():
            return self.response_exception(code=SERVICE_CODE_CUSTOMER_NOT_EXIST)
        if active_flag:
            change_active.active_flag = active_flag
        return self.response(self.response_success({
                "customer_id": change_active.id,
                "customer_active_flag": change_active.active_flag
            }))

    def delete_account(self, request):
        if not request.body:
            return self.response_exception(code=SERVICE_CODE_NOT_EXISTS_BODY)
        try:
            content = self.decode_to_json(request.body)
        except Exception as ex:
            return self.response_exception(code=SERVICE_CODE_BODY_PARSE_ERROR, mess=str(ex))
        account_id = content.get('account_id')
        delete = Customer.objects.filter(id=account_id, deleted_flag=False).first()
        if delete:
            book_user = Customer_shoes.objects.filter(user_id=account_id, deleted_flag=False)
            if book_user:
                book_user.update(deleted_flag=True)
            delete.deleted_flag = True
            delete.save()
            return self.response(self.response_success("Success!"))
        else:
            return self.response_exception(code=SERVICE_CODE_CUSTOMER_NOT_EXIST)
