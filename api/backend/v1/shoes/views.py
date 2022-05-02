import datetime
from django.db.models import F, Q
from api.base.apiViews import APIView
from config.settings import DATA_UPLOAD_MAX_MEMORY_SIZE
from core.postgres.shoes_store.customer.models import Customer_shoes
from core.postgres.shoes_store.shoes.models import (
    Shoes,
    Shoes_category,
    Shoes_discount,
    Shoes_quantity
)
from library.constant.api import (
    SERVICE_CODE_BODY_PARSE_ERROR,
    SERVICE_CODE_NOT_EXISTS_BODY,
    SERVICE_CODE_NOT_FOUND,
    SERVICE_CODE_FILE_SIZE,
    SERVICE_CODE_FORMAT_NOT_SUPPORTED,
    SERVICE_CODE_SHOES_NOT_EXIST,
)
from library.functions import (
    convert_string_to_list,
    convert_to_int,
    convert_to_float,
    convert_byte_to_base64
)
from library.service.upload_file import get_constant_file_type_from_extension


class ShoesStore(APIView):
    def list_shoes(self, request):
        shoes_name = self.request.query_params.get('shoes_name')
        category_id = self.request.query_params.get('category_id')
        brand_id = self.request.query_params.get('brand_id')
        gender = self.request.query_params.get('gender') # 1 male, 2 female
        date_check = datetime.now()
        shoes_list = Shoes.objects.filter(deleted_flag=False)
        if shoes_name:
            shoes_list = shoes_list.filter(name__icontains=shoes_name)
        if category_id:
            shoes_list = shoes_list.filter(category_id=category_id)
        if brand_id:
            shoes_list = shoes_list.filter(brand_id=brand_id)
        if gender:
            shoes_list = shoes_list.filter(gender=gender)

        shoes_list = shoes_list.annotate(
            shoes_id=F('id'),
            shoes_name=F('shoes_name'),
            shoes_code=F('shoes_code'),
            category_name=F('category__name'),
            brand_name=F('brand__name'),
        ).values(
            'shoes_id',
            'shoes_name',
            'shoes_code',
            'category_id',
            'category_name',
            'brand_id',
            'brand_name',
            'gender',
            'retail_price',
            'image_bytes'
        ).order_by('shoes_id')
        for shoes in shoes_list:
            discount = Shoes_discount.objects.get(
                shoes_id=shoes['shoes_id'],
                end_discount_date__gte=date_check,
                deleted_flag=False
            )
            if discount:
                sale_price = shoes['retail_price'] * ((100 - discount.discount_percent)/100)
                shoes['discount_percent'] = discount.discount_percent
                shoes['sale_price'] = sale_price
            base64 = convert_byte_to_base64(shoes['image_bytes'])
            shoes['image_bytes'] = base64
        self.pagination(shoes_list)
        return self.response(self.response_paging(self.paging_list))

    def detail_shoes(self, request):
        shoes_id = convert_to_int(self.request.query_params.get('shoes_id'))
        shoes = Shoes.objects.filter(id=shoes_id, deleted_flag=False)
        date_check = datetime.now()
        if shoes:
            shoes = shoes.annotate(
                shoes_id=F('id'),
                shoes_name=F('shoes_name'),
                shoes_code=F('shoes_code'),
                category_name=F('category__name'),
                brand_name=F('brand__name'),
            ).values(
                'shoes_id',
                'shoes_name',
                'shoes_code',
                'gender',
                'description',
                'retail_price',
                'brand_id',
                'brand_name',
                'image_bytes'
            ).order_by('shoes_id').first()
            shoes['image_bytes'] = convert_byte_to_base64(shoes['image_bytes'])
            # get shoes category
            shoes_category = Shoes_category.objects.filter(
                shoes_id=shoes['id'],
                deleted_flag=False
            ).annotate(
                category_name=F('category__name')
            ).values(
                # "shoes_id",
                "category_id",
                "category_name"
            )
            # get shoes quantity
            shoes_quantity = Shoes_quantity.objects.filter(
                shoes_id=shoes['id'],
                deleted_flag=False
            ).values(
                # "shoes_id",
                "size",
                "quantity"
            )
            # get shoes discount
            shoes_discount = Shoes_discount.objects.filter(
                shoes_id=shoes['id'],
                end_discount_date__gte=date_check,
                deleted_flag=False
            ).values(
                # "shoes_id",
                "discount_percent",
                "end_discount_date"
            )
            result = {
                "info_shoes": {
                    "shoes_id": shoes['id'],
                    "shoes_name": shoes['name'],
                    "shoes_code": shoes['code'],
                    "shoes_gender": shoes['gender'],
                    "shoes_description": shoes['description'],
                    "shoes_retail_price": shoes['retail_price'],
                    "shoes_brand_id": shoes['brand_id'],
                    "shoes_brand_name": shoes['brand_name'],
                    "shoes_imagebytes": shoes['image_bytes']
                },
                "shoes_category": list(shoes_category),
                "shoes_quantity": list(shoes_quantity),
                "shoes_discount": shoes_discount,
            }
            return self.response(self.response_success(result))
        else:
            return self.response_exception(code=SERVICE_CODE_NOT_FOUND)

    def shoes_same_category(self, request):
        shoes_id = convert_to_int(self.request.query_params.get('shoes_id'))
        try:
            shoes = Shoes.objects.get(id=shoes_id, deleted_flag=False)
        except Shoes.DoesNotExist:
            return self.response_exception(code=SERVICE_CODE_NOT_FOUND, mess="Shoes not found!")
        try:
            shoes_category = Shoes_category.objects.get(shoes_id=shoes.id, deleted_flag=False)
        except Shoes_category.DoesNotExist:
            return self.response_exception(code=SERVICE_CODE_NOT_FOUND, mess="Shoes_category not found!")

        shoes_same_category = Shoes.objects.filter(
            ~Q(id=shoes.id),
            Q(category_id=shoes_category.category_id),
            Q(deleted_flag=False)
        ).values(
            'id',
            'name',
            'code',
            'gender',
            'retail_price',
            'image_bytes'
        ).order_by('id')
        for item in shoes_same_category:
            base64 = convert_byte_to_base64(item['image_bytes'])
            item['image_bytes'] = base64
        return self.response(self.response_success(list(shoes_same_category)))

    def create_or_update(self, request):
        if not request.data:
            return self.response_exception(code=SERVICE_CODE_NOT_EXISTS_BODY)
        try:
            content = request.data
        except:
            return self.response_exception(code=SERVICE_CODE_BODY_PARSE_ERROR)

        key_content_list = list(content.keys())
        check_keys_list = ['name', 'code', 'gender', 'category_id', 'brand_id', 'retail_price', 'wholesale_price', 'size', 'quantity']
        shoes_id = content.get('shoes_id')
        name = content.get('name')
        code = content.get('code')
        description = content.get('description')
        retail_price = convert_to_float(content.get('price'))
        wholesale_price = convert_to_float(content.get('price'))
        category_id = content.get('category_id')
        brand_id = convert_to_int(content.get('brand_id'))
        gender = convert_to_int(content.get('gender'))
        size_quantity = content.get('size_quantity')
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
        if shoes_id:
            try:
                shoes = Shoes.objects.get(id=shoes_id, deleted_flag=False)
            except Shoes.DoesNotExist:
                return self.response_exception(code=SERVICE_CODE_NOT_FOUND)
            shoes.name = name if name is not None else shoes.name
            shoes.description = description if description is not None else shoes.description
            shoes.code = code if code is not None else shoes.code
            shoes.gender = gender if gender > 0 else shoes.gender
            shoes.brand_id = brand_id if brand_id > 0 else shoes.brand_id
            shoes.retail_price = retail_price if retail_price > 0.0 else shoes.retail_price
            shoes.wholesale_price = wholesale_price if wholesale_price > 0 else shoes.wholesale_price
            if image:
                shoes.image_bytes = image.read()
            shoes.save()
            if category_id:
                for cate in category_id:
                    try:
                        shoes_cate = Shoes_category.objects.get(shoes_id=shoes_id, category_id=cate, deleted_falg=False)
                    except Shoes_category.DoesNotExist():
                        return self.response_exception(code=SERVICE_CODE_NOT_FOUND)
                    shoes_cate.category_id = cate if cate > 0 else shoes_cate.category_id
                shoes_cate.save()
            return self.response(self.response_success({"shoes_id": shoes.id}))
        else:
            if not all(key in key_content_list for key in check_keys_list):
                return self.validate_exception(
                    'Missing ' + ", ".join(str(param) for param in check_keys_list if param not in key_content_list))

            if not description:
                description = ""

            shoes_new = Shoes.objects.create(
                name=name,
                code=code,
                gender=gender,
                description=description,
                retail_price=retail_price,
                wholesale_price=wholesale_price,
                brand_id=brand_id,
                image_bytes=image.read()
            )
            for cate in category_id:
                shoes_cate = Shoes_category.objects.create(
                    shoes=shoes_new.id,
                    category_id=cate
                )
            return self.response(self.response_success({"shoes_id": shoes_new.id}))

    def delete_shoes(self, request):
        if not request.body:
            return self.response_exception(code=SERVICE_CODE_NOT_EXISTS_BODY)
        try:
            content = self.decode_to_json(request.body)
        except Exception as ex:
            return self.response_exception(code=SERVICE_CODE_BODY_PARSE_ERROR, mess=str(ex))
        shoes_id = content.get('shoes_id')
        delete = Shoes.objects.filter(id=shoes_id, deleted_flag=False).first()
        if delete:
            shoes_user = Customer_shoes.objects.filter(shoes_id=shoes_id, deleted_flag=False)
            if shoes_user:
                shoes_user.update(deleted_flag=True)
            delete.deleted_flag = True
            delete.save()
            return self.response(self.response_success("Success!"))
        else:
            return self.response_exception(code=SERVICE_CODE_SHOES_NOT_EXIST)