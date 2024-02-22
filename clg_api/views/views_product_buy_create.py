import json
from datetime import datetime
from rest_framework.decorators import APIView
from rest_framework.authentication import TokenAuthentication
from clg_api.models import Order, Product, Province, District
from user.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from clg_api import globalparamers
import logging
from clg_api.validation import validation_product_buy_create

logger = logging.getLogger('django')


class ProductBuyCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        if not request.body:
            message = {
                globalparamers.RESULT_CODE: globalparamers.UNSUCESS_CODE,
                globalparamers.RESULT_DESCRIPTION: globalparamers.NO_REQUEST_BODY
            }
            return JsonResponse(message, status=status.HTTP_400_BAD_REQUEST)
        rating = validation_product_buy_create.product_buy_validate(
            request, pk)
        try:
            data = json.loads(request.body)
            print('data', data)
            province = str(data["province"]).strip(
            ) if 'province' in data else ''
            if province:
                province = Province.objects.get(id=province)
                province_name = province.name
            district = str(data["district"]).strip(
            ) if 'district' in data else ''
            if district:
                district = District.objects.get(
                    id=district, province_id=province)
                district_name = district.name
            street = str(data["street"]).strip() if 'street' in data else ''
            quantity = str(data['quantity']).strip(
            ) if 'quantity' in data else ''
            if not quantity:
                quantity = 0
            if street and province_name and district_name:
                full_order_address = province_name + district_name + street
                user = User.objects.get(id=request.user)
                user.order_location = full_order_address
                user.save()
            print('data', data)
            customer_id = User.objects.get(id=request.user.id)
            product_id = Product.objects.get(id=pk)
            product_id = Product.objects.get(id=pk)
            vendor_id = User.objects.get(id=product_id.vendor_id.id)
            if Order.objects.filter(product__id=product_id, customer__id=customer_id).exists():
                order = Order.objects.get(
                    product__id=product_id, customer__id=customer_id)
                order.rating = rating
                order.save()
            else:
                Order.objects.create(customer=customer_id,
                                     product=product_id,
                                     vendor_id=vendor_id,
                                     created_by=customer_id,
                                     rating=rating,
                                     quantity=quantity,
                                     creaed_at=datetime.now())
            message = {
                globalparamers.RESULT_CODE: globalparamers.SUCCESS_CODE,
                globalparamers.RESULT_DESCRIPTION: globalparamers.SUCCESS_RESULT_DESCRIPTION
            }
            return JsonResponse(message, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(str(e), exc_info=True)
            message = {
                globalparamers.RESULT_CODE: globalparamers.UNSUCESS_CODE,
                globalparamers.RESULT_DESCRIPTION: globalparamers.ERROR_MESSAGE
            }
            return JsonResponse(message, status=status.HTTP_400_BAD_REQUEST)
