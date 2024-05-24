from rest_framework.response import Response
from rest_framework.views import APIView
from common.utils import HelperMethods, LogHelper


class LoggerAPIView(APIView, HelperMethods, LogHelper):
    """APIView with Logger"""

    def send_200(self, data):
        return Response(data, 200)

    def send_500(self, message="Something went wrong"):
        data = {
            "message": message
        }
        return Response(data, 500)

    def send_400(self, message="Couldn't find any data", code="UNKNOWN"):
        data = {
            "message": message,
            "code": code
        }
        return Response(data, 400)

