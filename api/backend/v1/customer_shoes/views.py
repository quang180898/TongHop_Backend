from django.db.models import F
from api.base.apiViews import APIView
from core.postgres.shoes_store.shoes.models import Shoes, Shoes_image, Shoes_quantity
from core.postgres.shoes_store.customer.models import Customer, Customer_shoes
from library.constant.api import (
    SERVICE_CODE_NOT_EXISTS_BODY,
    SERVICE_CODE_BODY_PARSE_ERROR,
    SERVICE_CODE_NOT_FOUND,
    SERVICE_CODE_SHOES_NOT_EXIST,
    SERVICE_CODE_CUSTOMER_NOT_EXIST,
    SERVICE_CODE_SHOES_USER_NOT_EXIST
)
from library.functions import convert_to_int, convert_byte_to_base64


class AccountShoes(APIView):
    def history(self, request):
        customer_id = convert_to_int(self.request.query_params.get('customer_id'))
        sort_key = convert_to_int(self.request.query_params.get('sort_key'))
        account_shoes = Customer_shoes.objects.filter(customer_id=customer_id, deleted_flag=False)
        if sort_key == 1:
            account_shoes = account_shoes.annotate(
                shoes_name=F('shoes__name'),
                customer_name=F('customer__name')
            ).values(
                'id',
                'shoes_id',
                'shoes_name',
                'price',
                'total',
                'size',
                'quantity',
                'customer_id',
                'customer_name',
                'address',
                'created_at'
            ).order_by('-created_at')
        elif sort_key == 0:
            account_shoes = account_shoes.annotate(
                shoes_name=F('shoes__name'),
                customer_name=F('customer__name')
            ).values(
                'id',
                'shoes_id',
                'shoes_name',
                'price',
                'total',
                'size',
                'quantity',
                'customer_id',
                'customer_name',
                'address',
                'created_at'
            ).order_by('created_at')
        else:
            account_shoes = account_shoes.annotate(
                shoes_name=F('shoes__name'),
                customer_name=F('customer__name')
            ).values(
                'id',
                'shoes_id',
                'shoes_name',
                'price',
                'total',
                'size',
                'quantity',
                'customer_id',
                'customer_name',
                'address',
                'created_at'
            ).order_by('id')
        self.pagination(account_shoes)
        return self.response(self.response_paging(self.paging_list))

    def list_shoes_account(self, request):
        sort_key = convert_to_int(self.request.query_params.get('sort_key'))
        account_shoes = Customer_shoes.objects.filter(deleted_flag=False)
        if sort_key == 1:
            account_shoes = account_shoes.annotate(
                shoes_name=F('shoes__name'),
                customer_name=F('customer__name')
            ).values(
                'id',
                'shoes_id',
                'shoes_name',
                'price',
                'total',
                'size',
                'quantity',
                'customer_id',
                'customer_name',
                'address',
                'created_at'
            ).order_by('-created_at')
        elif sort_key == 0:
            account_shoes = account_shoes.annotate(
                shoes_name=F('shoes__name'),
                customer_name=F('customer__name')
            ).values(
                'id',
                'shoes_id',
                'shoes_name',
                'price',
                'total',
                'size',
                'quantity',
                'customer_id',
                'customer_name',
                'address',
                'created_at'
            ).order_by('created_at')
        else:
            account_shoes = account_shoes.annotate(
                shoes_name=F('shoes__name'),
                customer_name=F('customer__name')
            ).values(
                'id',
                'shoes_id',
                'shoes_name',
                'price',
                'total',
                'size',
                'quantity',
                'customer_id',
                'customer_name',
                'address',
                'created_at'
            ).order_by('id')
        self.pagination(account_shoes)
        return self.response(self.response_paging(self.paging_list))
    
    def detail_shoes_account(self, request):
        customer_shoes_id = convert_to_int(self.request.query_params.get('customer_shoes_id'))
        account_shoes = Customer_shoes.objects.filter(
            id=customer_shoes_id,
            deleted_flag=False
        )
        if account_shoes:
            account_shoes= account_shoes.annotate(
                shoes_name=F('shoes__name'),
                customer_name=F('customer__name')
            ).values(
                'id',
                'shoes_id',
                'shoes_name',
                'price',
                'total',
                'size',
                'quantity',
                'customer_id',
                'customer_name',
                'address',
                'created_at'
            ).first()
            return self.response(self.response_success(account_shoes))
        else:
            self.response_exception(code=SERVICE_CODE_NOT_FOUND)

    def most_buy(self, request):
        shoes_most_buy = Shoes.objects.filter(
            deleted_flag=False
        ).values(
            'id',
            'name',
            'gender',
            'retail_price'
        )
        for item in shoes_most_buy:
            image = Shoes_image.objects.filter(
                shoes_id=item['id'],
                deleted_flag=False
            ).first()
            if image:
                item['image_bytes'] = image.get_image
            shoes_count = Customer_shoes.objects.filter(shoes_id=item['id']).values('shoes_id', 'quantity')
            count = 0
            for count_quantity in shoes_count:
                count += count_quantity['quantity']
            item['count_buy'] = count
        # sap xep tu cao den thap
        sort = sorted(shoes_most_buy, key=lambda key: key['count_buy'], reverse=True)
        return self.response(self.response_success(sort))

    def create(self, request):
        if not request.body:
            return self.response_exception(code=SERVICE_CODE_NOT_EXISTS_BODY)
        try:
            content = self.decode_to_json(request.body)
        except Exception as ex:
            return self.response_exception(code=SERVICE_CODE_BODY_PARSE_ERROR, mess=str(ex))

        customer_id = content['customer_id']
        address = content['address']
        discount_code = content.get('discount_code', None)

        try:
            Customer.objects.get(id=customer_id, deleted_flag=False, active_flag=True)
        except Customer.DoesNotExist:
            return self.response_exception(code=SERVICE_CODE_CUSTOMER_NOT_EXIST)

        list_create = []
        list_update_size_quantity = []
        for item in content['order']:
            try:
                Shoes.objects.get(id=item['shoes_id'], deleted_flag=False)
            except Shoes.DoesNotExist:
                return self.validate_exception(code=SERVICE_CODE_SHOES_NOT_EXIST)

            # kiem tra so luong con lai co du ban hay khong
            try:
                shoes_quantity = Shoes_quantity.objects.get(
                    shoes_id=item['shoes_id'],
                    size=item['size'],
                    deleted_flag=False
                )
            except Shoes_quantity.DoesNotExist:
                return self.validate_exception("Không tìm thấy size!")

            quantity_update = int(shoes_quantity.quantity - item['quantity'])
            if quantity_update < 0:
                return self.validate_exception("Không đủ số lượng size giày còn lại để bán!")
            
            list_update_size_quantity.append(Shoes_quantity(
                id=shoes_quantity.id,
                quantity=quantity_update,
            ))
            if discount_code is not None:
                if discount_code == 'hpbd':
                    if item['quantity'] > 1:
                        self.validate_exception("Mã Khuyến mãi chỉ có thể mua 1 sản phẩm!")

                    total = int(item['price']*0.9)
                else:
                    total = int(item['quantity'] * item['price'])
            else:
                total = int(item['quantity'] * item['price'])

            list_create.append(Customer_shoes(
                shoes_id=item['shoes_id'],
                customer_id=customer_id,
                price=item['price'],
                total=total,
                quantity=item['quantity'],
                size=item['size'],
                address=address
            ))
        if discount_code is not None:
            if discount_code == 'hpbd':
                if len(list_create) > 1:
                    self.validate_exception("Mã Khuyến mãi chỉ có thể mua 1 sản phẩm!")
            else:
                self.validate_exception("Mã Khuyến mãi không tồn tại!")

        if list_create:
            Customer_shoes.objects.bulk_create(list_create)
        if list_update_size_quantity:
            Shoes_quantity.objects.bulk_update(list_update_size_quantity, fields=['quantity'])

        return self.response(self.response_success(True))

    def update_shoes_account(self, request):
        if not request.data:
            return self.response_exception(code=SERVICE_CODE_NOT_EXISTS_BODY)
        try:
            content = request.POST
        except Exception as ex:
            return self.response_exception(code=SERVICE_CODE_BODY_PARSE_ERROR, mess=str(ex))

        customer_shoes_id = convert_to_int(content.get('customer_shoes_id'))
        price = convert_to_int(content.get('price'))
        size = convert_to_int(content.get('size'))
        quantity = convert_to_int(content.get('quantity'))
        if customer_shoes_id:
            try:
                cus_shoes = Customer_shoes.objects.get(id=customer_shoes_id, deleted_flag=False)
            except Customer_shoes.DoesNotExist:
                return self.response_exception(code=SERVICE_CODE_SHOES_NOT_EXIST)
            cus_shoes.price = price if price > 0 else cus_shoes.price
            cus_shoes.size = size if size > 0 else cus_shoes.size
            cus_shoes.quantity = quantity if quantity > 0 else cus_shoes.quantity
            cus_shoes.total = cus_shoes.quantity * cus_shoes.price
            cus_shoes.save()
            return self.response(self.response_success({
                "id": cus_shoes.id,
                "customer_id": cus_shoes.customer_id,
                "shoes_id": cus_shoes.shoes_id,
                "price": cus_shoes.price,
                "total": cus_shoes.total,
                "quantity": cus_shoes.quantity,
                "size": cus_shoes.size
            }))
        else:
            self.validate_exception("Missing customer_shoes_id")


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
