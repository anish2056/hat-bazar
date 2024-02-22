from clg_api.models import Product,Category, SubCategory
from clg_api import validations
from user.models import User
from rest_framework.decorators import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db import transaction
from django.http import JsonResponse

from clg_api import globalparamers
import logging


logger = logging.getLogger('django')
# Create your views here.



class  ProductCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if not request.body:
            message = {
                globalparamers.RESULT_CODE: globalparamers.UNSUCESS_CODE,
                globalparamers.RESULT_DESCRIPTION: globalparamers.NO_REQUEST_BODY
            }
            return JsonResponse(message, status=status.HTTP_400_BAD_REQUEST)
        try:
            (json_error, product_name, product, sub_product, description, product_prize,
             manufactured_date, image) = validations.product_validation(request, None)
            if json_error:
                message = {
                    globalparamers.RESULT_CODE: globalparamers.UNSUCESS_CODE,
                    globalparamers.RESULT_DESCRIPTION: globalparamers.UNSUCCESS_RESULT_DESCRIPTION,
                    "error": json_error
                }
                return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)
            user = User.objects.get(id=request.user)
            with transaction.atomic():
                sid = transaction.savepoint()
                if product:
                    category = Category.objects.get(id=product)
                    sub_category = SubCategory.objects.get(id=sub_product)
                else:
                    category= None
                    sub_category = None
                Product.objects.create(name=product_name,
                                       price=product_prize,
                                       description=description,
                                       category=category,
                                       sub_category=sub_category,
                                       photo=image,
                                       manufactured_date=manufactured_date,
                                       created_by_id=user,
                                       vendor_id=user
                                       )
                transaction.savepoint_commit(sid)
                message = {
                    globalparamers.RESULT_CODE: globalparamers.SUCCESS_CODE,
                    globalparamers.RESULT_DESCRIPTION: globalparamers.DATA_CREATE
                }
                return JsonResponse(message, status=status.HTTP_200_OK)
        except Exception as e:
            transaction.savepoint_rollback(sid)
            logger.error(str(e), exc_info=True)
            message = {
                globalparamers.RESULT_CODE: globalparamers.UNSUCESS_CODE,
                globalparamers.RESULT_DESCRIPTION: globalparamers.ERROR_MESSAGE
            }
            return JsonResponse(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

