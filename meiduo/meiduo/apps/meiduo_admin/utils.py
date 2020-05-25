#生成token
def jwt_response_payload_handler(token, user=None, request=None): #重写系统方法
    return {
        'token': token,
        'id': user.id,
        'username': user.username
    }


#自定义分页类
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
class PageNum(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'pagesize'
    max_page_size = 10

    def get_paginated_response(self, data):
        return Response({
            'count':self.page.paginator.count,
            'lists':data,
            'page':self.page.number,
            'pages':self.page.paginator.num_pages,
            'pagesize':self.page_size
        })