import ast
from datetime import datetime
from django.db.models import F, Q
from api.base.apiViews import APIView
from config.settings import DATA_UPLOAD_MAX_MEMORY_SIZE
from core.postgres.shoes_store.category.models import Category
from core.postgres.shoes_store.customer.models import Customer_shoes
from core.postgres.shoes_store.shoes.models import (
    Brand,
    Shoes,
    Shoes_discount,
    Shoes_image,
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
    def list_home(self, request):
        date_check = datetime.now()
        shoes_list = Shoes.objects.filter(
            deleted_flag=False
        ).annotate(
            shoes_id=F('id'),
            shoes_name=F('name'),
            shoes_code=F('code'),
            shoes_brand_id=F('brand'),
            shoes_brand_name=F('brand__name'),
            shoes_category_id=F('category'),
            shoes_category_name=F('category__name')
        ).values(
            'shoes_id',
            'shoes_name',
            'shoes_code',
            'shoes_brand_id',
            'shoes_brand_name',
            'gender',
            'retail_price'
        ).order_by('shoes_id')
        for shoes in shoes_list:
            brand_image = Brand.objects.filter(
                id=shoes['shoes_brand_id'],
                deleted_flag=False
            ).first()
            if brand_image:
                shoes['shoes_brand_image'] = brand_image.get_image
                    
            shoes_quantity = Shoes_quantity.objects.filter(
                shoes_id=shoes['shoes_id'],
                deleted_flag=False
            ).values(
                "size",
                "quantity"
            )
            if shoes_quantity:
                list_size = []
                for si in shoes_quantity:
                    list_size.append({
                        "size": si['size'],
                        "quantity": si['quantity']
                    })
                shoes["shoes_quantity"] = list_size
            discount = Shoes_discount.objects.filter(
                shoes_id=shoes['shoes_id'],
                end_discount_date__gte=date_check,
                deleted_flag=False
            ).first()
            if discount:
                shoes['discount_percent'] = discount.discount_percent
                shoes['sale_price'] = int(shoes['retail_price'] * ((100 - discount.discount_percent)/100))
            else:
                shoes['discount_percent'] = 0
                shoes['sale_price'] = shoes['retail_price']
            image = Shoes_image.objects.filter(
                shoes_id=shoes['shoes_id'],
                deleted_flag=False
            ).first()
            if image:
                base64 = image.get_image
                shoes['image_bytes'] = base64

        test = self.nested_object_list(
            shoes_list,
            mapping_key='shoes_brand_id',
            fields={
                'list_shoes': [
                    'shoes_id',
                    'shoes_name',
                    'shoes_code',
                    'gender',
                    'retail_price',
                    'shoes_quantity',
                    'discount_percent',
                    'sale_price',
                    'image_bytes'
                ]})
        return self.response(self.response_success(list(test)))

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
            shoes_name=F('name'),
            shoes_code=F('code'),
            shoes_brand_id=F('brand'),
            shoes_brand_name=F('brand__name'),
            shoes_category_id=F('category'),
            shoes_category_name=F('category__name')
        ).values(
            'shoes_id',
            'shoes_name',
            'shoes_code',
            'shoes_brand_id',
            'shoes_brand_name',
            'gender',
            'retail_price'
        ).order_by('shoes_id')
        for shoes in shoes_list:
            shoes_quantity = Shoes_quantity.objects.filter(
                shoes_id=shoes['shoes_id'],
                deleted_flag=False
            ).values(
                "size",
                "quantity"
            )
            if shoes_quantity:
                list_size = []
                for si in shoes_quantity:
                    list_size.append({
                        "size": si['size'],
                        "quantity": si['quantity']
                    })
                shoes["shoes_quantity"] = list_size
            discount = Shoes_discount.objects.filter(
                shoes_id=shoes['shoes_id'],
                end_discount_date__gte=date_check,
                deleted_flag=False
            ).first()
            if discount:
                shoes['discount_percent'] = discount.discount_percent
                shoes['sale_price'] = int(shoes['retail_price'] * ((100 - discount.discount_percent)/100))
            else:
                shoes['discount_percent'] = 0
                shoes['sale_price'] = shoes['retail_price']
            image = Shoes_image.objects.filter(
                shoes_id=shoes['shoes_id'],
                deleted_flag=False
            ).first()
            if image:
                base64 = image.get_image
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
                shoes_name=F('name'),
                shoes_code=F('code'),
                shoes_brand_name=F('brand__name'),
                shoes_brand_id=F('brand'),
                shoes_category_id=F('category'),
                shoes_category_name=F('category__name')
            ).values(
                'shoes_id',
                'shoes_name',
                'shoes_code',
                'gender',
                'description',
                'retail_price',
                'shoes_brand_id',
                'shoes_brand_name',
                'shoes_category_id',
                'shoes_category_name',
            ).first()

            image = Shoes_image.objects.filter(
                shoes_id=shoes['shoes_id'],
                deleted_flag=False
            ).values(
                'id',
                'image_bytes'
            )
            image_list = []
            for img in image:
                image_list.append({
                    "image_id": img['id'],
                    "image_bytes": convert_byte_to_base64(img['image_bytes'])
                })
            shoes['image_bytes'] = image_list
            # get shoes quantity
            shoes_quantity = Shoes_quantity.objects.filter(
                shoes_id=shoes['shoes_id'],
                deleted_flag=False
            ).values(
                "size",
                "quantity"
            )
            # get shoes discount
            shoes_discount = Shoes_discount.objects.filter(
                shoes_id=shoes['shoes_id'],
                end_discount_date__gte=date_check,
                deleted_flag=False
            )
            if shoes_discount:
                shoes_discount = shoes_discount.values(
                    "discount_percent",
                    "end_discount_date"
                    ).first()

                sale_price = int(shoes['retail_price'] * ((100 - shoes_discount['discount_percent'])/100))

                result = {
                    "shoes_id": shoes['shoes_id'],
                    "shoes_name": shoes['shoes_name'],
                    "shoes_code": shoes['shoes_code'],
                    "gender": shoes['gender'],
                    "shoes_description": shoes['description'],
                    "retail_price": shoes['retail_price'],
                    "shoes_brand_id": shoes['shoes_brand_id'],
                    "shoes_brand_name": shoes['shoes_brand_name'],
                    "shoes_category_id": shoes['shoes_category_id'],
                    "shoes_category_name": shoes['shoes_category_name'],
                    "image_bytes": shoes['image_bytes'],
                    "shoes_quantity": list(shoes_quantity),
                    "sale_price": sale_price,
                    "discount_percent": shoes_discount['discount_percent'],
                    "end_discount_date": shoes_discount['end_discount_date']
                }
            else:
                result = {
                    "shoes_id": shoes['shoes_id'],
                    "shoes_name": shoes['shoes_name'],
                    "shoes_code": shoes['shoes_code'],
                    "gender": shoes['gender'],
                    "shoes_description": shoes['description'],
                    "retail_price": shoes['retail_price'],
                    "shoes_brand_id": shoes['shoes_brand_id'],
                    "shoes_brand_name": shoes['shoes_brand_name'],
                    "shoes_category_id": shoes['shoes_category_id'],
                    "shoes_category_name": shoes['shoes_category_name'],
                    "image_bytes": shoes['image_bytes'],
                    "shoes_quantity": list(shoes_quantity),
                    "sale_price": None,
                    "discount_percent": None,
                    "end_discount_date": None
                }
            return self.response(self.response_success(result))
        else:
            return self.response_exception(code=SERVICE_CODE_NOT_FOUND)

    def shoes_same_category(self, request):
        shoes_id = convert_to_int(self.request.query_params.get('shoes_id'))
        try:
            shoes = Shoes.objects.get(id=shoes_id, deleted_flag=False)
        except Shoes.DoesNotExist:
            return self.response_exception(code=SERVICE_CODE_NOT_FOUND)
        date_check = datetime.now()
        shoes_same_category = Shoes.objects.filter(
            ~Q(id=shoes.id),
            Q(category_id=shoes.category_id),
            Q(deleted_flag=False)
        )
        if shoes_same_category:
            shoes_same_category = shoes_same_category.annotate(
                shoes_id=F('id'),
                shoes_name=F('name'),
                shoes_code=F('code'),
                shoes_gender=F('gender'),
                shoes_brand_id=F('brand'),
                shoes_brand_name=F('brand__name')
            ).values(
                'shoes_id',
                'shoes_name',
                'shoes_code',
                'gender',
                'retail_price'
            ).order_by('shoes_id')
            for item in shoes_same_category:
                shoes_quantity = Shoes_quantity.objects.filter(
                    shoes_id=item['shoes_id'],
                    deleted_flag=False
                ).values(
                    "size",
                    "quantity"
                )
                if shoes_quantity:
                    list_size = []
                    for si in shoes_quantity:
                        list_size.append({
                            "size": si['size'],
                            "quantity": si['quantity']
                        })
                    item["shoes_quantity"] = list_size
                discount = Shoes_discount.objects.filter(
                    shoes_id=item['shoes_id'],
                    end_discount_date__gte=date_check,
                    deleted_flag=False
                ).first()
                if discount:
                    item['discount_percent'] = discount.discount_percent
                    item['sale_price'] = int(item['retail_price'] * ((100 - discount.discount_percent)/100))
                else:
                    item['discount_percent'] = 0
                    item['sale_price'] = item['retail_price']
                image = Shoes_image.objects.filter(
                    shoes_id=item['shoes_id'],
                    deleted_flag=False
                ).first()
                if image:
                    base64 = image.get_image
                    item['image_bytes'] = base64
            self.pagination(shoes_same_category)
            return self.response(self.response_paging(self.paging_list))
        else:
            return self.response(self.response_paging(list))

    def create_or_update(self, request):
        if not request.data:
            return self.response_exception(code=SERVICE_CODE_NOT_EXISTS_BODY)
        try:
            content = request.data
        except:
            return self.response_exception(code=SERVICE_CODE_BODY_PARSE_ERROR)

        key_content_list = list(content.keys())
        check_keys_list = ['name', 'code', 'gender', 'category_id', 'brand_id', 'retail_price', 'wholesale_price', 'size_quantity']
        shoes_id = content.get('shoes_id')
        name = content.get('name')
        code = content.get('code')
        description = content.get('description')
        retail_price = convert_to_int(content.get('retail_price'))
        wholesale_price = convert_to_int(content.get('wholesale_price'))
        category_id = convert_to_int(content.get('category_id'))
        brand_id = convert_to_int(content.get('brand_id'))
        gender = convert_to_int(content.get('gender'))
        size_quantity = content.get('size_quantity')
        image = request.FILES.getlist('image', None)
        if image:
            for img in image:
                img_format = str(img).split('.')[-1]
                image_name = get_constant_file_type_from_extension(img_format)
                if image_name is None:
                    return self.response_exception(code=SERVICE_CODE_FORMAT_NOT_SUPPORTED)
                size = request.headers['content-length']
                if int(size) > DATA_UPLOAD_MAX_MEMORY_SIZE:
                    return self.response_exception(code=SERVICE_CODE_FILE_SIZE, mess=f"size of {img} > 2.5MB!")
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
            shoes.category_id = category_id if category_id > 0 else shoes.category_id
            shoes.retail_price = retail_price if retail_price > 0.0 else shoes.retail_price
            shoes.wholesale_price = wholesale_price if wholesale_price > 0 else shoes.wholesale_price
            if image:
                for img in image:
                    Shoes_image.objects.create(
                        shoes_id=shoes_id,
                        image_bytes=img.read()
                    )
            shoes.save()
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
                category_id=category_id
            )
            for img in image:
                Shoes_image.objects.create(
                    shoes_id=shoes_new.id,
                    image_bytes=img.read()
                )
            Shoes_discount.objects.create(
                shoes_id=shoes_new.id,
                discount_percent=0,
                end_discount_date=datetime.now()
            )
            for qs in ast.literal_eval(size_quantity):
                Shoes_quantity.objects.create(
                    shoes_id=shoes_new.id,
                    size=qs['size'],
                    quantity=qs['quantity']
                )
            return self.response(self.response_success({"shoes_id": shoes_new.id}))

    def delete_shoes(self, request):
        if not request.body:
            return self.response_exception(code=SERVICE_CODE_NOT_EXISTS_BODY)
        try:
            content = self.decode_to_json(request.body)
        except Exception as ex:
            return self.response_exception(code=SERVICE_CODE_BODY_PARSE_ERROR, mess=str(ex))
        shoes_id = convert_to_int(content.get('shoes_id'))
        delete = Shoes.objects.filter(id=shoes_id, deleted_flag=False).first()
        if delete:
            shoes_user = Customer_shoes.objects.filter(shoes_id=shoes_id, deleted_flag=False)
            if shoes_user:
                shoes_user.update(deleted_flag=True)
            shoes_image = Shoes_image.objects.filter(shoes_id=shoes_id, deleted_flag=False)
            if shoes_image:
                shoes_image.update(deleted_flag=True)
            shoes_discount = Shoes_discount.objects.filter(shoes_id=shoes_id, deleted_flag=False)
            if shoes_discount:
                shoes_discount.update(deleted_flag=True)
            shoes_size_quantity = Shoes_quantity.objects.filter(shoes_id=shoes_id, deleted_flag=False)
            if shoes_size_quantity:
                shoes_size_quantity.update(deleted_flag=True)
            delete.deleted_flag = True
            delete.save()
            return self.response(self.response_success("Success!"))
        else:
            return self.response_exception(code=SERVICE_CODE_SHOES_NOT_EXIST)