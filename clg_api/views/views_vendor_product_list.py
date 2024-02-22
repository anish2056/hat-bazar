from clg_api.models import Order, Product
from rest_framework.decorators import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.http import JsonResponse

from clg_api import globalparamers
import logging


logger = logging.getLogger('django')
# Create your views here.


class VendorProductListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            from django.db.models import Count
            vendor_product_list = []
            products = Order.objects.filter(vendor_id=request.user)
            for product in products:
                product = Product.objects.get(id=product.product)
                vendor_product_list.append({
                    "id": product.id,
                    "name": product.name,
                    "price": product.price,
                    # "photo": base64.b64encode(product.photo).decode("utf-8") if product.photo else None,
                    "description": product.description,
                    "date_created": product.manufactured_date,
                })

            message = {
                globalparamers.RESULT_CODE: globalparamers.SUCCESS_CODE,
                globalparamers.RESULT_DESCRIPTION: globalparamers.SUCCESS_RESULT_DESCRIPTION,
                "data": vendor_product_list
            }
            print("vendor data", )
            return JsonResponse(message, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(str(e), exc_info=True)
            message = {
                globalparamers.RESULT_CODE: globalparamers.UNSUCESS_CODE,
                globalparamers.RESULT_DESCRIPTION: globalparamers.ERROR_MESSAGE
            }
            return JsonResponse(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
