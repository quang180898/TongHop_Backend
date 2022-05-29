from django.db.models import F
from api.base.apiViews import APIView
from config.settings import DATA_UPLOAD_MAX_MEMORY_SIZE
from core.postgres.shoes_store.shoes.models import Brand
from library.constant.api import (
    SERVICE_CODE_BODY_PARSE_ERROR,
    SERVICE_CODE_BRAND_NOT_EXIST,
    SERVICE_CODE_FILE_SIZE,
    SERVICE_CODE_FORMAT_NOT_SUPPORTED,
    SERVICE_CODE_NOT_EXISTS_BODY,
    SERVICE_CODE_NOT_FOUND
)
from library.functions import convert_byte_to_base64, convert_to_int
from library.service.upload_file import get_constant_file_type_from_extension


class ShoesBrand(APIView):
    def list_brand(self, request):
        brand_list = Brand.objects.filter(
            deleted_flag=False
        ).annotate(
            brand_id=F('id'),
            brand_name=F('name'),
            brandy_description=F('description')
        ).values(
            'brand_id',
            'brand_name',
            'image_bytes',
            'brand_description'
        ).order_by('brand_id')
        for img in brand_list:
            base64 = convert_byte_to_base64(img['image_bytes'])
            brand_list['image_bytes'] = base64
        self.pagination(brand_list)
        return self.response(self.response_paging(self.paging_list))

    def detail_brand(self, request):
        brand_id = convert_to_int(self.request.query_params.get('brand_id'))
        brand = Brand.objects.filter(
            id=brand_id,
            deleted_flag=False
        )
        if brand:
            brand= brand.annotate(
                brand_id=F('id'),
                brand_name=F('name'),
                brand_description=F('description')
            ).values(
                'brand_id',
                'brand_name',
                'image_bytes',
                'brand_description'
            ).first()
            base64 = convert_byte_to_base64(brand['image_bytes'])
            brand['image_bytes'] = base64
            return self.response(self.response_success(brand))
        else:
            return self.response_exception(code=SERVICE_CODE_BRAND_NOT_EXIST)

    def create_or_update(self, request):
        if not request.data:
            return self.response_exception(code=SERVICE_CODE_NOT_EXISTS_BODY)
        try:
            content = request.data
        except Exception as ex:
            return self.response_exception(code=SERVICE_CODE_BODY_PARSE_ERROR, mess=str(ex))
        
        key_content_list = list(content.keys())
        check_keys_list = ['name', 'image']

        brand_id = convert_to_int(content.get('brand_id'))
        name = content.get('name')
        description = content.get('description')
        image = request.FILES.get('image', None)
        if image:
            img_format = str(image).split('.')[-1]
            image_name = get_constant_file_type_from_extension(img_format)
            if image_name is None:
                return self.response_exception(code=SERVICE_CODE_FORMAT_NOT_SUPPORTED)
            size = request.headers['content-length']
            if int(size) > DATA_UPLOAD_MAX_MEMORY_SIZE:
                return self.response_exception(code=SERVICE_CODE_FILE_SIZE)
        if brand_id:
            try:
                brand = Brand.objects.get(id=brand_id, deleted_flag=False)
            except Brand.DoesNotExist:
                return self.response_exception(code=SERVICE_CODE_NOT_FOUND)
            brand.name = name if name is not None else brand.name
            brand.image_bytes = image.read() if image is not None else brand.image_bytes
            brand.description = description if description is not None else brand.description
            brand.save()
            return self.response(self.response_success({
                "brand_id": brand.id,
                "brand_name": brand.name,
                "brand_image_bytes": brand.image_bytes,
                "brand_description": brand.description
            }))
        else:
            if not all(key in key_content_list for key in check_keys_list):
                return self.validate_exception(
                    'Missing ' + ", ".join(str(param) for param in check_keys_list if param not in key_content_list))

            if description is None:
                description = ""

            brand = Brand.objects.create(
                name=name,
                image_bytes=image.read(),
                description=description
            )
            return self.response(self.response_success({
                "brand_id": brand.id,
                "brand_name": brand.name,
                "brand_image_bytes": brand.image_bytes,
                "brand_description": brand.description
            }))

    def delete_brand(self, request):
        if not request.body:
            return self.response_exception(code=SERVICE_CODE_NOT_EXISTS_BODY)
        try:
            content = self.decode_to_json(request.body)
        except Exception as ex:
            return self.response_exception(code=SERVICE_CODE_BODY_PARSE_ERROR, mess=str(ex))
        brand_id = convert_to_int(content.get('brand_id'))
        brand = Brand.objects.filter(id=brand_id, deleted_flag=False).first()
        if brand:
            brand.deleted_flag = True
            brand.save()
            return self.response(self.response_success("Success!"))
        else:
            return self.response_exception(code=SERVICE_CODE_BRAND_NOT_EXIST)
