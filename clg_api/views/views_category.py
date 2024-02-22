from clg_api import custom_exception
from clg_api.models import Category
from user.models import User
from rest_framework.decorators import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.http import JsonResponse

from clg_api import globalparamers
import logging

logger = logging.getLogger('django')
# Create your views here.


class CategoryListView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            categorys = Category.objects.all()
            category_list = []
            for category in categorys:
                category_list.append({
                    "id": category.id,
                    "name": category.name
                })
            message = {
                globalparamers.RESULT_CODE: globalparamers.SUCCESS_CODE,
                globalparamers.RESULT_DESCRIPTION: globalparamers.SUCCESS_RESULT_DESCRIPTION,
                "data": category_list
            }
            print('data',category_list)
            return JsonResponse(message, status=status.HTTP_200_OK)
        except Exception as e:
            message = custom_exception.custom_exception(request, e)


class UserCategoryListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            categorys = User.objects.filter(id=request.user).values('category')
            category_list = []
            for category in categorys:
                user_category = Category.objects.get(id=category['category'])
                category_list.append({
                    "id": category['category'],
                    "name": user_category.name
                })
            message = {
                globalparamers.RESULT_CODE: globalparamers.SUCCESS_CODE,
                globalparamers.RESULT_DESCRIPTION: globalparamers.SUCCESS_RESULT_DESCRIPTION,
                "data": category_list
            }
            return JsonResponse(message, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(str(e), exc_info=True)
            message = custom_exception.custom_exception(request, e)
            return JsonResponse(message, status=status.HTTP_400_BAD_REQUEST)
