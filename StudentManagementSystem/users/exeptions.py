from rest_framework.exceptions import APIException

class ItemNotFoundException(APIException):
    status_code = 404
    default_detail = 'Item not found.'
    default_code = 'item_not_found'
