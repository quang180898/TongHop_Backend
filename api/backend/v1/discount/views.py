from datetime import datetime
from django.db.models import F
from api.base.apiViews import APIView
from core.postgres.shoes_store.shoes.models import Shoes, Shoes_discount
from library.constant.api import (
    SERVICE_CODE_BODY_PARSE_ERROR,
    SERVICE_CODE_DISCOUNT_NOT_EXIST,
    SERVICE_CODE_NOT_EXISTS_BODY,
    SERVICE_CODE_NOT_FOUND,
    SERVICE_CODE_PRODUCT_DISCOUNT_EXIST,
    SERVICE_CODE_RECORD_NOT_VALIDATE
)
from library.functions import convert_to_int, string_to_time


class ShoesDiscount(APIView):
    def list_discount(self, request):
        discount = Shoes_discount.objects.filter(
            deleted_flag=False
        ).annotate(
            discount_id=F('id'),
            shoes_name=F('shoes__name'),
        ).values(
            'discount_id',
            'shoes_id',
            'shoes_name',
            'discount_percent',
            'end_discount_date',
        ).order_by('-end_discount_date')
        self.pagination(discount)
        return self.response(self.response_paging(self.paging_list))
    
    def detail_discount(self, request):
        discount_id = convert_to_int(self.request.query_params.get('discount_id'))
        discount = Shoes_discount.objects.filter(
            id=discount_id,
            deleted_flag=False
        )
        if discount:
            discount = discount.annotate(
                discount_id=F('id'),
                shoes_name=F('shoes__name')
            ).values(
                'discount_id',
                'shoes_id',
                'shoes_name',
                'discount_percent',
                'end_discount_date'
            ).first()
            return self.response(self.response_success(discount))
        else:
            return self.response_exception(code=SERVICE_CODE_DISCOUNT_NOT_EXIST)

    def update_discount(self, request):
        if not request.data:
            return self.response_exception(code=SERVICE_CODE_NOT_EXISTS_BODY)
        try:
            content = request.data
        except Exception as ex:
            return self.response_exception(code=SERVICE_CODE_BODY_PARSE_ERROR, mess=str(ex))
        key_content_list = list(content.keys())
        check_keys_list = ['shoes_id', 'percent', 'end_discount_date']
        shoes_id = convert_to_int(content.get('shoes_id'))
        percent = convert_to_int(content.get('percent'))
        end_discount_date = content.get('end_discount_date')

        if not all(key in key_content_list for key in check_keys_list):
            return self.validate_exception(
                'Missing ' + ", ".join(str(param) for param in check_keys_list if param not in key_content_list))
        
        date_check = datetime.now()
        if end_discount_date:
            end_discount_date = string_to_time(end_discount_date, '%d/%m/%Y %H:%M:%S')
            if end_discount_date < date_check:
                return self.response_exception(code=SERVICE_CODE_RECORD_NOT_VALIDATE)
        try:
            shoes = Shoes.objects.get(id=shoes_id, deleted_flag=False)
        except Shoes.DoesNotExist:
            return self.response_exception(code=SERVICE_CODE_NOT_FOUND, mess="Shoes not exist!")
        try:
            discount = Shoes_discount.objects.get(shoes_id=shoes_id, deleted_flag=False)
        except Shoes_discount.DoesNotExist:
            return self.response_exception(code=SERVICE_CODE_NOT_FOUND, mess="Discount not exist!")

        discount.discount_percent = percent if percent >= 0 else discount.discount_percent
        discount.end_discount_date = end_discount_date if end_discount_date is not None else discount.end_discount_date
        discount.save()
        return self.response(self.response_success({
            "discount_id": discount.id,
            "shoes_id": discount.shoes_id,
            "discount_percent": discount.discount_percent,
            "end_discount_date": discount.end_discount_date
        }))

    def delete_discount(self, request):
        if not request.body:
            return self.response_exception(code=SERVICE_CODE_NOT_EXISTS_BODY)
        try:
            content = self.decode_to_json(request.body)
        except Exception as ex:
            return self.response_exception(code=SERVICE_CODE_BODY_PARSE_ERROR, mess=str(ex))
        discount_id = convert_to_int(content.get('discount_id'))
        discount = Shoes_discount.objects.filter(id=discount_id, deleted_flag=False).first()
        if discount:
            discount.deleted_flag = True
            discount.save()
            return self.response(self.response_success("Success!"))
        else:
            return self.response_exception(code=SERVICE_CODE_DISCOUNT_NOT_EXIST)
