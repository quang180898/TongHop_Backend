from django.core.paginator import Paginator, EmptyPage
from api.base.base_apiView import BaseAPIView
from api.base.authentication import TokenAuthentication
from library.constant.api import PAGINATOR_PER_PAGE
from rest_framework import HTTP_HEADER_ENCODING


class APIView(BaseAPIView):
    # setting default authentication
    # authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    user = None
    is_paging = False
    per_page = PAGINATOR_PER_PAGE
    page = 1
    total_page = None
    total_record = None
    paging_list = None
    current_page = None
    order_by = 'id'

    def dispatch(self, *args, **kwargs):
        response = super().dispatch(*args, **kwargs)
        # from django.db import connection
        # for query in connection.queries:
        #     print("\n")
        #     print(query["sql"])
        #     print("\n")
        # print(50*"=")
        # print("Total number of queries: ", end="")
        # print(len(connection.queries))
        # print(50*"=")
        return response

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.user = request.user
        self.parse_param_common(request)
        self.init_paging()

    def init_paging(self):
        per_page = self.request.query_params.get('limit', None)
        page = self.request.query_params.get('page', None)
        order_by = self.request.query_params.get('order_by', None)
        if type(order_by) is list:
            order_by = ",".join(map(str, self.order_by))
        if order_by and isinstance(order_by, str):
            self.order_by = order_by

        if per_page and per_page.isdigit():
            self.per_page = int(per_page)
        if page and page.isdigit():
            self.page = int(page)

    def pagination(self, query_set):
        is_order = getattr(query_set, 'ordered', None)
        if not is_order:
            try:
                query_set = query_set.order_by(self.order_by)
            except:
                self.order_by = '_id'
                query_set = query_set.order_by(self.order_by)

        paginator = Paginator(query_set, per_page=self.per_page)

        self.total_record = paginator.count
        self.total_page = paginator.num_pages
        self.is_paging = True
        try:
            self.paging_list = list(paginator.page(self.page))
        except EmptyPage:
            self.paging_list = []


class APIAnonymousView(BaseAPIView):
    # authentication_classes = ()
    permission_classes = list()
