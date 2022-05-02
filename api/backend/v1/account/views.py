import re

from django.contrib.auth.hashers import make_password, check_password
from django.db.models import F

from api.base.apiViews import APIView
from config.settings import DATA_UPLOAD_MAX_MEMORY_SIZE
from core.postgres.library.book.models import BookUser
from core.postgres.library.customer.models import Customer
from core.postgres.library.permission.models import Permission
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
from library.functions import convert_to_int, is_mobile_valid, convert_byte_to_base64
from library.service.upload_file import get_constant_file_type_from_extension


class Account(APIView):
    def list_user(self, request):
        user_list = Customer.objects.filter(
            deleted_flag=False
        ).annotate(
            permission_code=F('permission__code'),
            permission_name=F('permission__name')
        ).values(
            'id',
            'name',
            'mobile',
            'username',
            'mail',
            'permission_code',
            'permission_name'
        ).order_by('id')
        return self.response(self.response_success(list(user_list)))

    def info_user(self, request):
        user_id = convert_to_int(self.request.query_params.get('user_id'))
        customer = Customer.objects.filter(
            id=user_id,
            deleted_flag=False
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
            'permission_name'
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
        if len(user_name) < 4 or len(user_name) > 25:
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
            permission_id=2,
            image_bytes=image.read()
        )
        permission = Permission.objects.filter(
            code=user_new.permission_id
        ).values(
            'code',
            'name'
        ).first()

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
        mail = content.get("mail")
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
            customer.mail = mail if mail is not None else customer.mail
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
            book_user = BookUser.objects.filter(user_id=account_id, deleted_flag=False)
            if book_user:
                book_user.update(deleted_flag=True)
            delete.deleted_flag = True
            delete.save()
            return self.response(self.response_success("Success!"))
        else:
            return self.response_exception(code=SERVICE_CODE_CUSTOMER_NOT_EXIST)
    # def info_user(self, request):
    #     param = request.query_params
    #     key_content_list = list(param.keys())
    #     user_id = convert_to_int(param.get('user_id'))
    #     if 'user_id' in key_content_list:
    #         cus_permission = Customer.objects.filter(
    #                 id=user_id,
    #                 deleted_flag=False
    #             ).values(
    #                 'id',
    #                 'permission__code',
    #                 'permission__name',
    #                 'name',
    #                 'avatar_url',
    #                 'mobile',
    #                 'username',
    #                 'password',
    #                 'email'
    #             ).first()
    #         if cus_permission:
    #             vms = VMS.objects.filter(
    #                 deleted_flag=False
    #             ).annotate(
    #                 vms_id=F('id'),
    #                 vms_name=F('name'),
    #                 vms_longitude=F('longitude'),
    #                 vms_latitude=F('latitude')
    #             ).values(
    #                 'vms_id',
    #                 'vms_name',
    #                 'vms_longitude',
    #                 'vms_latitude'
    #             )
    #             for a in vms:
    #                 group = VmsGroup.objects.filter(
    #                     vms=a['vms_id'],
    #                     deleted_flag=False
    #                 ).annotate(
    #                     group_id=F('id'),
    #                     group_name=F('name')
    #                 ).values(
    #                     'group_id',
    #                     'group_name')
    #                 a['list_group'] = list(group)
    #                 for i in group:
    #                     camera = Camera.objects.filter(
    #                         camera_group_id=i['group_id'],
    #                         deleted_flag=False,
    #                         active_flag=True
    #                     ).annotate(
    #                         camera_id=F('id'),
    #                         camera_name=F('name'),
    #                         camera_slug=F('slug'),
    #                         view_flag=Case(When(Subquery(CameraUser.objects.filter(
    #                             user_id=user_id,
    #                             camera_id=OuterRef('id'),
    #                             deleted_flag=False).values('active_flag')), then=True),
    #                             default=Value(False),
    #                             output_field=BooleanField()),
    #                         edit_flag=Case(When(Subquery(CameraUser.objects.filter(
    #                             user_id=user_id,
    #                             camera_id=OuterRef('id'),
    #                             deleted_flag=False).values('edit_flag')), then=True),
    #                             default=Value(False),
    #                             output_field=BooleanField()),
    #                     ).values(
    #                         'camera_id',
    #                         'camera_name',
    #                         'camera_slug',
    #                         'view_flag',
    #                         'edit_flag',
    #                         'url_stream'
    #                     ).order_by('camera_id')
    #                     i['list_camera'] = list(camera)
    #                     if cus_permission['permission__code'] == ADMIN or cus_permission['permission__code'] == MANAGER:
    #                         for item in list(camera):
    #                             item['view_flag'] = True
    #                             item['edit_flag'] = True
    #             user_avatar_url = ""
    #             # if cus_permission['avatar_url']:
    #             #     user_avatar_url = CLOUD_SERVER_URL + cus_permission['avatar_url']
    #             tmp = {
    #                 "info_user": {
    #                     "user_id": cus_permission['id'],
    #                     "user_name": cus_permission['name'],
    #                     "user_permission_code": cus_permission['permission__code'],
    #                     "user_permission_name": cus_permission['permission__name'],
    #                     "user_username": cus_permission['username'],
    #                     "user_password": cus_permission['password'],
    #                     "user_mobile": cus_permission['mobile'],
    #                     "user_email": cus_permission['email'],
    #                     "user_avatar_url": user_avatar_url
    #                 },
    #                 "info_camera": list(vms)
    #             }
    #             return self.response(self.response_success(tmp))
    #         else:
    #             return self.response_exception(code=SERVICE_CODE_CUSTOMER_NOT_EXIST)
    #     else:
    #         return self.validate_exception("Missing user_id!")
    #
    # def list_user(self, request):
    #     cus_permission = Customer.objects.filter(id=self.user.id, deleted_flag=False).values('permission__code').first()
    #     if not cus_permission:
    #         return self.response_exception(code=SERVICE_CODE_CUSTOMER_NOT_EXIST)
    #     user_full_name = self.request.query_params.get('user_full_name')
    #     if cus_permission['permission__code'] != USER:
    #         user = Customer.objects.filter(
    #             ~Q(id=self.user.id),
    #             Q(permission__code__in=[USER, MANAGER]),
    #             Q(deleted_flag=False)
    #         )
    #         if user_full_name:
    #             user = user.filter(name__icontains=user_full_name)
    #         user = user.annotate(
    #             user_id=F('id'),
    #             user_full_name=F('name'),
    #             user_username=F('username'),
    #             user_mobile=F('mobile'),
    #             user_email=F('email'),
    #             user_permission_id=F('permission'),
    #             user_permission_code=F('permission__code'),
    #             user_permission_name=F('permission__name'),
    #             user_active_flag=F('active_flag')
    #         ).values(
    #             'user_id',
    #             'user_full_name',
    #             'user_mobile',
    #             'user_email',
    #             'user_username',
    #             'user_permission_id',
    #             'user_permission_code',
    #             'user_permission_name',
    #             'user_active_flag'
    #         ).order_by('user_id')
    #         self.pagination(user)
    #         return self.response(self.response_paging(self.paging_list))
    #     else:
    #         return self.response_exception(code=SERVICE_CODE_USER_PERMISSION)
    #
    # def vms_of_admin(self, request):
    #     user_id = self.user.id
    #     camera_name = self.request.query_params.get('camera_name')
    #     tmp = {}
    #     cus_permission = Customer.objects.filter(id=user_id, deleted_flag=False).values('permission__code').first()
    #     if not cus_permission:
    #         return self.response_exception(code=SERVICE_CODE_CUSTOMER_NOT_EXIST)
    #     system_location = SystemLocation.objects.filter().values(
    #         'id',
    #         'latitude',
    #         'longitude',
    #         'image_url'
    #     ).first()
    #     vms = VMS.objects.filter(
    #         deleted_flag=False
    #     ).annotate(
    #         vms_id=F('id'),
    #         vms_name=F('name'),
    #         vms_host=F('host'),
    #         vms_port=F('port'),
    #         vms_streaming_port=F('streaming_port'),
    #         vms_proxy_directory=F('proxy_directory')
    #     ).values(
    #         'vms_id',
    #         'vms_name',
    #         'vms_host',
    #         'vms_port',
    #         'vms_streaming_port',
    #         'vms_proxy_directory',
    #     ).order_by('vms_id')
    #     for a in vms:
    #         group = VmsGroup.objects.filter(
    #             vms=a['vms_id'],
    #             deleted_flag=False
    #         ).annotate(
    #             group_id=F('id'),
    #             group_name=F('name'),
    #             group_image_url=Case(When(
    #                 image_url__isnull=False,
    #                 then=Concat(Value(CLOUD_SERVER_URL), F('image_url'))),
    #                 default=None
    #             ),
    #         ).values(
    #             'group_id',
    #             'group_name',
    #             'group_image_url'
    #         ).order_by('group_id')
    #         a['list_group'] = list(group)
    #         for i in group:
    #             if camera_name:
    #                 camera = Camera.objects.filter(
    #                     camera_group_id=i['group_id'],
    #                     name__icontains=camera_name,
    #                     deleted_flag=False,
    #                     active_flag=True
    #                 )
    #             else:
    #                 camera = Camera.objects.filter(
    #                     camera_group_id=i['group_id'],
    #                     deleted_flag=False,
    #                     active_flag=True
    #                 )
    #             camera = camera.annotate(
    #                 camera_id=F('id'),
    #                 camera_name=F('name'),
    #                 camera_slug=F('slug'),
    #                 vms_proxy_directory=F('vms__proxy_directory'),
    #                 view_flag=Case(When(Subquery(CameraUser.objects.filter(
    #                     user_id=user_id,
    #                     camera_id=OuterRef('id'),
    #                     deleted_flag=False).values('active_flag')), then=True),
    #                                default=Value(False),
    #                                output_field=BooleanField()),
    #                 edit_flag=Case(When(Subquery(CameraUser.objects.filter(
    #                     user_id=user_id,
    #                     camera_id=OuterRef('id'),
    #                     deleted_flag=False).values('edit_flag')), then=True),
    #                                default=Value(False),
    #                                output_field=BooleanField()),
    #             ).values(
    #                 'vms_id',
    #                 'camera_id',
    #                 'camera_name',
    #                 'camera_slug',
    #                 'view_flag',
    #                 'edit_flag',
    #                 'url_stream',
    #                 'vms_proxy_directory'
    #             ).order_by('camera_id')
    #             for tmp in camera:
    #                 url = tmp['url_stream']
    #                 tmp['url_stream'] = LOCAL_SERVER_DOMAIN + '/cctv_api/' + tmp['vms_proxy_directory'] + '/' + url
    #             i['list_camera'] = list(camera)
    #             if cus_permission['permission__code'] == ADMIN or cus_permission['permission__code'] == MANAGER:
    #                 for item in list(camera):
    #                     item['view_flag'] = True
    #                     item['edit_flag'] = True
    #         tmp = {
    #             'layout_url': CLOUD_SERVER_URL + system_location['image_url'] if system_location['image_url'] is not None else "",
    #             'longitude': system_location['longitude'],
    #             'latitude': system_location['latitude'],
    #             'list_vms': list(vms)
    #         }
    #     return self.response(self.response_success(tmp))
    #
    # def create_or_update(self, request):
    #     if not request.data:
    #         return self.response_exception(code=SERVICE_CODE_NOT_EXISTS_BODY)
    #     try:
    #         content = request.POST
    #     except Exception as ex:
    #         return self.response_exception(code=SERVICE_CODE_BODY_PARSE_ERROR, mess=str(ex))
    #     if content == {}:
    #         return self.response_exception(code=SERVICE_CODE_BODY_PARSE_ERROR)
    #     key_content_list = list(content.keys())
    #     check_keys_list = ['user_name', 'pass_word', 'password_repeat', 'name',
    #                        'email', 'mobile']
    #
    #     user_id = convert_to_int(content['user_id'] if content.get('user_id') else None)
    #     name = content['name'] if content.get('name') else None
    #     mobile = content['mobile'] if content.get('mobile') else None
    #     email = content['email'] if content.get('email') else None
    #     image = request.FILES.get('image')
    #     user_permission_type = convert_to_int(content['user_permission_type'] if content.get('user_permission_type') else None)
    #     user_name = content['user_name'] if content.get('user_name') else None
    #     pass_word = content['pass_word'] if content.get('pass_word') else None
    #     password_repeat = content['password_repeat'] if content.get('password_repeat') else None
    #     camera_obj = convert_to_dict(content['camera_obj'] if content.get('camera_obj') else None)
    #     # check permission user
    #     cus_permission = Customer.objects.filter(id=self.user.id, deleted_flag=False).values('permission__code').first()
    #     if not cus_permission:
    #         return self.response_exception(code=SERVICE_CODE_CUSTOMER_NOT_EXIST)
    #     if cus_permission['permission__code'] == USER:
    #         return self.response_exception(code=SERVICE_CODE_USER_PERMISSION)
    #     # ---------------------
    #     if image and image.size > settings.DATA_UPLOAD_MAX_MEMORY_SIZE:
    #         return self.response_exception(code=SERVICE_CODE_FILE_SIZE)
    #     if name and name.isspace():
    #         return self.validate_exception("name must have characters!!!")
    #     if mobile:
    #         if mobile.isspace():
    #             return self.validate_exception("mobile must have characters!!!")
    #         if not is_mobile_valid(mobile):
    #             return self.response_exception(code=SERVICE_CODE_MOBILE_LENGTH)
    #         if Customer.objects.filter(mobile=mobile, deleted_flag=False).exists():
    #             return self.response_exception(code=SERVICE_CODE_USER_MOBILE_DUPLICATE)
    #     if email:
    #         if email.isspace():
    #             return self.validate_exception("email must have characters!!!")
    #         if ' ' in email:
    #             return self.validate_exception("email not have space!!!")
    #         if Customer.objects.filter(email=email, deleted_flag=False).exists():
    #             return self.response_exception(code=SERVICE_CODE_USER_EMAIL_DUPLICATE)
    #     if user_name and user_name.isspace():
    #         return self.validate_exception("user_name must have characters!!!")
    #     if user_permission_type:
    #         if user_permission_type > 3 or user_permission_type < 1:
    #             return self.validate_exception("1 < permission < 3")
    #     if user_id:
    #         response = []
    #         edit_account = Customer.objects.filter(
    #             id=user_id,
    #             deleted_flag=False
    #         ).first()
    #         if not edit_account:
    #             return self.response_exception(code=SERVICE_CODE_CUSTOMER_NOT_EXIST)
    #         permission_code = Permission.objects.filter(id=edit_account.permission_id).values('code').first()
    #         # kiem tra quyen user dang login
    #         check_permission = Customer.objects.filter(id=self.user.id, deleted_flag=False).values('permission__code').first()
    #         if check_permission['permission__code'] == permission_code['code']:
    #             return self.response_exception(code=SERVICE_CODE_SAME_LEVEL_USER_EDIT)
    #         edit_account.name = name if name is not None else edit_account.name
    #         edit_account.mobile = mobile if mobile is not None else edit_account.mobile
    #         edit_account.email = email if email is not None else edit_account.email
    #         if user_permission_type != 0 and cus_permission['permission__code'] == ADMIN:
    #             edit_account.permission_id = user_permission_type
    #         edit_account.save()
    #         if image:
    #             image_name = request.data.get('image_name', None)
    #             if not image_name:
    #                 return self.response_exception(code=SERVICE_CODE_IMAGE_NAME_REQUIRED)
    #             img = image_name.split('.')[-1]
    #             image_name = get_constant_file_type_from_extension(img)
    #             if not image_name:
    #                 return self.response_exception(code=SERVICE_CODE_FORMAT_NOT_SUPPORTED)
    #             size = request.headers['content-length']
    #             if int(size) > settings.DATA_UPLOAD_MAX_MEMORY_SIZE:
    #                 return self.response_exception(code=SERVICE_CODE_FILE_SIZE)
    #             try:
    #                 edit_account.put_avatar(image)
    #             except Exception as ex:
    #                 return self.validate_exception(str(ex))
    #         if camera_obj:
    #             list_camera_id = [temp['camera_id'] for temp in camera_obj]
    #             camera_check = Camera.objects.filter(id__in=list_camera_id, deleted_flag=False)
    #             if len(camera_check) != len(list_camera_id):
    #                 return self.validate_exception("Some library is not exists!")
    #             camera_user_obj = CameraUser.objects.filter(
    #                 user_id=user_id,
    #                 camera_id__in=list_camera_id,
    #                 deleted_flag=False
    #             ).values(
    #                 'id',
    #                 'camera_id')
    #             camera_user = {temp['camera_id']: temp['id'] for temp in camera_user_obj}
    #             list_create = []
    #             list_create_vmsuser = []
    #             list_update = []
    #             # check permission
    #             cus_permission = Customer.objects.filter(id=edit_account.id, deleted_flag=False).values(
    #                 'permission__code').first()
    #             if not cus_permission:
    #                 return self.response_exception(code=SERVICE_CODE_CUSTOMER_NOT_EXIST)
    #             if cus_permission['permission__code'] == MANAGER:
    #                 for cam in camera_obj:
    #                     if cam['camera_id'] in camera_user:
    #                         list_update.append(CameraUser(pk=camera_user.get(cam['camera_id']),
    #                                                       active_flag=cam['view_flag'],
    #                                                       edit_flag=cam['view_flag']))
    #                     else:
    #                         list_create.append(CameraUser(camera_id=cam['camera_id'],
    #                                                       user_id=user_id,
    #                                                       active_flag=cam['view_flag'],
    #                                                       edit_flag=cam['view_flag']))
    #             elif cus_permission['permission__code'] == USER:
    #                 for cam in camera_obj:
    #                     if cam['camera_id'] in camera_user:
    #                         list_update.append(CameraUser(pk=camera_user.get(cam['camera_id']),
    #                                                       active_flag=cam['view_flag'],
    #                                                       edit_flag=False))
    #                     else:
    #                         list_create.append(CameraUser(camera_id=cam['camera_id'],
    #                                                       user_id=user_id,
    #                                                       active_flag=cam['view_flag'],
    #                                                       edit_flag=False))
    #
    #             if list_create:
    #                 CameraUser.objects.bulk_create(list_create)
    #             if list_update:
    #                 CameraUser.objects.bulk_update(list_update, fields=['active_flag', 'edit_flag'])
    #             # check xem user da ton tai trong bang user_vms hay chua
    #             list_vms_id = list(set(Camera.objects.filter(id__in=list_camera_id,
    #                                                          deleted_flag=False).values_list('vms_id', flat=True)))
    #             vms_check = list(set(VmsUser.objects.filter(user_id=user_id,
    #                                                         vms_id__in=list_vms_id,
    #                                                         deleted_flag=False,
    #                                                         active_flag=True
    #                                                         ).values_list('vms_id', flat=True)))
    #             list_vms_check = []
    #             for a in list_vms_id:
    #                 if a not in vms_check:
    #                     list_vms_check.append(a)
    #             if list_vms_check:
    #                 for item in list_vms_check:
    #                     list_create_vmsuser.append(VmsUser(user_id=user_id,
    #                                                        vms_id=item,
    #                                                        deleted_flag=False,
    #                                                        active_flag=True))
    #                 VmsUser.objects.bulk_create(list_create_vmsuser)
    #             response = camera_user_obj.annotate(
    #                 view_flag=F('active_flag')
    #             ).values(
    #                 'id',
    #                 'user_id',
    #                 'camera_id',
    #                 'view_flag'
    #             )
    #         permission = Permission.objects.filter(code=edit_account.permission_id).values('code', 'name').first()
    #         return self.response(self.response_success({
    #             "user_id": edit_account.id,
    #             "name": edit_account.name,
    #             "username": edit_account.username,
    #             "password": edit_account.password,
    #             "email": edit_account.email,
    #             "mobile": edit_account.mobile,
    #             "permission_code": permission['code'],
    #             "permission_name": permission['name'],
    #             "avatar_url": CLOUD_SERVER_URL + edit_account.avatar_url if edit_account.avatar_url is not None else "",
    #             "camera_list": list(response) if response else []
    #         }))
    #     else:
    #         cam_list = []
    #         if not all(key in key_content_list for key in check_keys_list):
    #             return self.validate_exception(
    #                 'Missing ' + ", ".join(str(param) for param in check_keys_list if param not in key_content_list))
    #         if Customer.objects.filter(username=user_name, deleted_flag=False).exists():
    #             return self.response_exception(code=SERVICE_CODE_USER_NAME_DUPLICATE)
    #         if user_name is None or ' ' in user_name:
    #             self.validate_exception(code=USER_NAME_ERROR)
    #         if len(user_name) < 4 or len(user_name) > 25:
    #             self.validate_exception(code=USER_NAME_LENGTH)
    #         if pass_word is None or ' ' in pass_word:
    #             self.validate_exception(code=NEW_PASSWORD_EMPTY)
    #         if len(pass_word) < 8 or len(pass_word) > 25:
    #             self.validate_exception(code=PASSWORD_LENGTH)
    #         if pass_word != password_repeat:
    #             self.validate_exception(code=INVALID_REPEAT_PASSWORD)
    #         if name is None:
    #             return self.validate_exception("name is not null!!!")
    #         if mobile is None:
    #             return self.validate_exception("mobile is not null!!!")
    #         if email is None:
    #             return self.validate_exception("email is not null!!!")
    #         if user_name is None:
    #             return self.validate_exception("user_name is not null!!!")
    #         if cus_permission['permission__code'] == ADMIN:
    #             if not user_permission_type:
    #                 return self.validate_exception("Missing permission_id!!!")
    #             user_new = Customer.objects.create(
    #                 name=name,
    #                 username=user_name,
    #                 password=make_password(pass_word),
    #                 mobile=mobile,
    #                 email=email,
    #                 permission_id=user_permission_type,
    #                 mobile_confirmed_flag=True,
    #                 email_confirmed_flag=True,
    #                 created_by=self.user.name)
    #         else:
    #             user_new = Customer.objects.create(
    #                 name=name,
    #                 username=user_name,
    #                 password=make_password(pass_word),
    #                 mobile=mobile,
    #                 email=email,
    #                 permission_id=USER,
    #                 mobile_confirmed_flag=True,
    #                 email_confirmed_flag=True,
    #                 created_by=self.user.name
    #             )
    #         if user_new:
    #             status_code, data = request_api(
    #                 CHATTING_SERVER + SERVICE_CHATTING_CREATE_URL,
    #                 method='post',
    #                 headers=CHATTING_SERVICE_HEAR,
    #                 content={
    #                     'system_user_id': user_new.id,
    #                     'username': user_new.username
    #                 })
    #         if image:
    #             image_name = request.data.get('image_name', None)
    #             if not image_name:
    #                 return self.response_exception(code=SERVICE_CODE_IMAGE_NAME_REQUIRED)
    #             img = image_name.split('.')[-1]
    #             image_name = get_constant_file_type_from_extension(img)
    #             if image_name is None:
    #                 return self.response_exception(code=SERVICE_CODE_FORMAT_NOT_SUPPORTED)
    #             size = request.headers['content-length']
    #             if int(size) > LIMIT_SIZE_IMAGE:
    #                 return self.response_exception(code=SERVICE_CODE_FILE_SIZE)
    #             try:
    #                 user_new.put_avatar(image)
    #             except Exception as ex:
    #                 return self.validate_exception(str(ex))
    #         if camera_obj:
    #             list_camera_id = [temp['camera_id'] for temp in camera_obj]
    #             user_create = user_new.id
    #             camera_user_obj = CameraUser.objects.filter(
    #                 user_id=user_create,
    #                 camera_id__in=list_camera_id,
    #                 deleted_flag=False
    #             ).values(
    #                 'id',
    #                 'camera_id'
    #             )
    #             camera_user = {temp['camera_id']: temp['id'] for temp in camera_user_obj}
    #             list_create = []
    #             list_create_vms = []
    #             for cam in camera_obj:
    #                 if cam['camera_id'] not in camera_user:
    #                     list_create.append(CameraUser(camera_id=cam['camera_id'],
    #                                                   user_id=user_create,
    #                                                   active_flag=cam['view_flag'],
    #                                                   edit_flag=False))
    #             if list_create:
    #                 CameraUser.objects.bulk_create(list_create)
    #             # create data in vms_user table
    #             vms = list(set(Camera.objects.filter(id__in=list_camera_id,
    #                                                  deleted_flag=False,
    #                                                  active_flag=True).values_list('vms_id', flat=True)))
    #             for item in vms:
    #                 list_create_vms.append(VmsUser(user_id=user_create, vms_id=item))
    #             if list_create_vms:
    #                 VmsUser.objects.bulk_create(list_create_vms)
    #             camera_user_obj = camera_user_obj.filter(
    #                 user_id=user_create,
    #                 deleted_flag=False
    #             ).annotate(view_flag=F('active_flag')).values(
    #                 'id',
    #                 'user_id',
    #                 'camera_id',
    #                 'view_flag'
    #             )
    #             for b in camera_user_obj:
    #                 cam_list.append({
    #                     "id": b['id'],
    #                     "user_id": b['user_id'],
    #                     "camera_id": b['camera_id'],
    #                     "view_flag": b['view_flag']
    #                 })
    #         permission = Permission.objects.filter(code=user_new.permission_id).values('code', 'name').first()
    #         return self.response(self.response_success({
    #             "user_id": user_new.id,
    #             "name": user_new.name,
    #             "mobile": user_new.mobile,
    #             "email": user_new.email,
    #             "user_name": user_new.username,
    #             "password": user_new.password,
    #             "permission_code": permission['code'],
    #             "permission_name": permission['name'],
    #             "cam_list": cam_list,
    #             "avatar_url": CLOUD_SERVER_URL + user_new.avatar_url if user_new.avatar_url is not None else ""
    #         }))
    #
    # def set_status(self, request):
    #     if not request.body:
    #         return self.response_exception(code=SERVICE_CODE_NOT_EXISTS_BODY)
    #     try:
    #         content = self.decode_to_json(request.body)
    #     except Exception as ex:
    #         return self.response_exception(code=SERVICE_CODE_BODY_PARSE_ERROR, mess=str(ex))
    #
    #     user_id = content.get('user_id')
    #     user_active_flag = content.get('user_active_flag')
    #     # check permission user
    #     cus_permission = Customer.objects.filter(id=self.user.id, deleted_flag=False).values('permission__code').first()
    #     if not cus_permission:
    #         return self.response_exception(code=SERVICE_CODE_CUSTOMER_NOT_EXIST)
    #     if cus_permission['permission__code'] == USER:
    #         return self.response_exception(code=SERVICE_CODE_USER_PERMISSION)
    #     # ---------------------
    #     user = Customer.objects.filter(deleted_flag=False, id=user_id).first()
    #     if not user:
    #         return self.response_exception(code=SERVICE_CODE_CUSTOMER_NOT_EXIST)
    #     check_permission = Permission.objects.filter(id=user.permission_id).values('code').first()
    #     if cus_permission['permission__code'] == check_permission['code']:
    #         return self.response_exception(code=SERVICE_CODE_SAME_LEVEL_USER_EDIT)
    #     if user_active_flag is not None:
    #         user.active_flag = user_active_flag
    #         user.save()
    #     return self.response(self.response_success({
    #         'user_id': user.id,
    #         'user_active_flag': user.active_flag
    #     }))
    #
    # def delete(self, request):
    #     if not request.body:
    #         return self.response_exception(code=SERVICE_CODE_NOT_EXISTS_BODY)
    #     try:
    #         content = self.decode_to_json(request.body)
    #     except Exception as ex:
    #         return self.response_exception(code=SERVICE_CODE_BODY_PARSE_ERROR, mess=str(ex))
    #     # check permission user
    #     cus_permission = Customer.objects.filter(id=self.user.id, deleted_flag=False).values('permission__code').first()
    #     if not cus_permission:
    #         return self.response_exception(code=SERVICE_CODE_CUSTOMER_NOT_EXIST)
    #     if cus_permission['permission__code'] == USER:
    #         return self.response_exception(code=SERVICE_CODE_USER_PERMISSION)
    #     # ---------------------
    #     user_id = content.get('user_id')
    #     delete = Customer.objects.filter(id=user_id, deleted_flag=False).first()
    #     if delete:
    #         permission_check = Permission.objects.filter(id=delete.permission_id).values('code').first()
    #         if cus_permission['permission__code'] == permission_check['code']:
    #             return self.response_exception(code=SERVICE_CODE_SAME_LEVEL_USER_DELETE)
    #         delete.deleted_flag = True
    #         delete.active_flag = False
    #         delete.save()
    #         camera_user = CameraUser.objects.filter(user_id=user_id, deleted_flag=False)
    #         if camera_user:
    #             camera_id_list = list(set(camera_user.values_list('camera_id', flat=True)))
    #             camera_user = camera_user.filter(camera_id__in=camera_id_list).update(deleted_flag=True,
    #                                                                                   active_flag=False)
    #         vms_user = VmsUser.objects.filter(user_id=user_id, deleted_flag=False)
    #         if vms_user:
    #             vms_user = vms_user.update(deleted_flag=True, active_flag=False)
    #         return self.response(self.response_delete())
    #     else:
    #         return self.response_exception(code=SERVICE_CODE_CUSTOMER_NOT_EXIST)
