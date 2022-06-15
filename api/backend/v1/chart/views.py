from api.base.apiViews import APIView
from django.db.models import F
from core.postgres.shoes_store.shoes.models import Shoes
from core.postgres.shoes_store.customer.models import Customer, Customer_shoes
from library.constant.api import (
    ADMIN,
    USER
)


class Chart(APIView):
    def all(self, request):
        admin = Customer.objects.filter(deleted_flag=False, permission__code=ADMIN)
        customer = Customer.objects.filter(deleted_flag=False, permission__code=USER)
        product = Shoes.objects.filter(deleted_flag=False)
        product_sell = Customer_shoes.objects.filter(deleted_flag=False)
        result = {
            "total_admin": len(admin),
            "total_customer": len(customer),
            "total_product": len(product),
            "total_product_sell": len(product_sell)
        }
        return self.response(self.response_success(result))

    def total(self, request):
        result = {}
        for item in range(1, 13):
            total_sell = 0
            product_sell = Customer_shoes.objects.filter(deleted_flag=False, created_at__month=item).values('total')
            if product_sell:
                for tt in product_sell:
                    total_sell += tt['total']
            result.update({
                f'month_{item}': total_sell
            })
        return self.response(self.response_success(result))

