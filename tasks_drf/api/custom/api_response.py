from rest_framework.utils.serializer_helpers import ReturnDict


class ApiResponse:

    @staticmethod
    def Success(data=None):
        response = {
            'error': None,
            'success': True,
            'data': data
        }
        return response

    @staticmethod
    def Error(message=None):
        response = {
            'error': message,
            'success': False,
            'data': None
        }
        return response