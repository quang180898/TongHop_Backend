from django.db.models import F
from api.base.apiViews import APIView
from core.postgres.shoes_store.shoes.models import Shoes, Shoes_quantity
from core.postgres.shoes_store.customer.models import Customer, Customer_shoes
from library.constant.api import (
    SERVICE_CODE_NOT_EXISTS_BODY,
    SERVICE_CODE_BODY_PARSE_ERROR,
    SERVICE_CODE_SHOES_NOT_EXIST,
    SERVICE_CODE_CUSTOMER_NOT_EXIST,
    SERVICE_CODE_SHOES_USER_NOT_EXIST
)
from library.functions import convert_to_int, convert_byte_to_base64


class AccountShoes(APIView):
    def list_shoes_account(self, request):
        account_shoes = Customer_shoes.objects.filter(deleted_flag=False)
        account_shoes = account_shoes.annotate(
            shoes_name=F('shoes__name'),
            customer_name=F('customer__name')
        ).values(
            'id',
            'shoes_id',
            'shoes_name',
            'size',
            'quantity',
            'customer_id',
            'customer_name',
            'created_at'
        ).order_by('-created_at')
        self.pagination(account_shoes)
        return self.response(self.response_paging(self.paging_list))
    
    def detail_shoes_account(self, request):
        customer_shoes_id = convert_to_int(self.request.query_params.get('customer_shoes_id'))
        account_shoes = Customer_shoes.objects.filter(
            id=customer_shoes_id,
            deleted_flag=False
        ).annotate(
            shoes_name=F('shoes__name'),
            customer_name=F('customer__name')
        ).values(
            'id',
            'shoes_id',
            'shoes_name',
            'size',
            'quantity',
            'customer_id',
            'customer_name',
            'created_at'
        )
        return self.response(self.response_success(account_shoes))

    def most_buy(self, request):
        shoes_most_buy = Shoes.objects.filter(
            deleted_flag=False
        ).values(
            'id',
            'name',
            'gender',
            'image_bytes',
            'retail_price'
        ).order_by('id')
        for item in shoes_most_buy:
            item['image_bytes'] = convert_byte_to_base64(item['image_bytes'])
            shoes_count = Customer_shoes.objects.filter(book_id=item['id'])
            item['count_buy'] = shoes_count.count()
        # sap xep tu cao den thap
        sort = sorted(shoes_most_buy, key=lambda key: key['count_buy'], reverse=True)
        return self.response(self.response_success(sort))

    def create_shoes_account(self, request):
        if not request.data:
            return self.response_exception(code=SERVICE_CODE_NOT_EXISTS_BODY)
        try:
            content = request.POST
        except Exception as ex:
            return self.response_exception(code=SERVICE_CODE_BODY_PARSE_ERROR, mess=str(ex))
        key_content_list = list(content.keys())
        check_keys_list = ['shoes_id', 'customer_id', 'size', 'retail_price', 'gender', 'quantity']

        shoes_id = convert_to_int(content.get('shoes_id'))
        customer_id = convert_to_int(content.get('customer_id'))
        retail_price = content.get('retail_price')
        size = content.get('size')
        gender = content.get('gender')
        quantity = content.get('quantity')
        if not all(key in key_content_list for key in check_keys_list):
            return self.validate_exception('Missing ' + ", ".join(str(param) for param in check_keys_list if param not in key_content_list))
        try:
            customer = Customer.objects.get(customer_id=customer_id, active_flag=True)
        except Customer.DoesNotExist():
            return self.response_exception(code=SERVICE_CODE_CUSTOMER_NOT_EXIST)
        if customer.active_flag == False:
            return self.validate_exception( "Người dùng không thể mua hàng chi tiết xin vui lòng liên hệ trực tiếp với shop!")
        try:
            shoes = Shoes.objects.get(id=shoes_id, deleted_flag=False)
        except Shoes.DoesNotExist():
            return self.response_exception(code=SERVICE_CODE_SHOES_NOT_EXIST)

        shoes_customer = Customer_shoes.objects.create(
            customer_id=customer_id,
            shoes_id=shoes_id,
            price=retail_price,
            gender=gender,
            quantity=quantity
        )

        try:
            shoes_quantity = Shoes_quantity.objects.get(shoes_id=shoes_id, size=size, deleted_flag=False)
        except Shoes_quantity.DoesNotExist():
            return self.validate_exception("Không tìm thấy size!")

        shoes_quantity.quantity = shoes_quantity.quantity - quantity
        if shoes_quantity.quantity < 0:
            return self.validate_exception("Không đủ số lượng size giày còn lại để bán!")
        else:
            shoes_quantity.save()
        return self.response(self.response_success({
            "customer_id": shoes_customer.customer_id,
            "shoes_id": shoes_customer.shoes_id,
            "price": shoes_customer.price,
            "quantity": shoes_customer.quantity,
            "gender": shoes_customer.gender,
            "size": shoes_customer.size,
        }))


    def delete_shoes_account(self, request):
        if not request.body:
            return self.response_exception(code=SERVICE_CODE_NOT_EXISTS_BODY)
        try:
            content = self.decode_to_json(request.body)
        except Exception as ex:
            return self.response_exception(code=SERVICE_CODE_BODY_PARSE_ERROR, mess=str(ex))

        customer_shoes_id = convert_to_int(content.get('customer_shoes_id'))
        customer_shoes = Customer_shoes.objects.filter(id=customer_shoes_id, deleted_flag=False).first()
        if customer_shoes:
            customer_shoes.deleted_flag = True
            customer_shoes.save()
            return self.response(self.response_success("Success!"))
        else:
            return self.response_exception(code=SERVICE_CODE_SHOES_USER_NOT_EXIST)
