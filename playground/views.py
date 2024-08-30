from django.shortcuts import render
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .tasks import sina
import logging

logger = logging.getLogger(__name__)


class TestChacheView(APIView):
    # @method_decorator(cache_page(5 * 0))
    def get(self, request):
        logger.warning("salam")
        response = requests.get("https://httpbin.org/delay/2")
        data = response.json()
        return Response({"detail": "dash"})
