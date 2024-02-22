import json
from pickle import TRUE
from clg_api.models import Product, SubCategory, Order, AddToCard
from clg_api import custom_exception
from rest_framework.decorators import APIView
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
import base64
from user.models import User
from django.db import connection
from clg_api.validation import validation_user_rating
from clg_api import login_auth
from clg_api import globalparamers
import logging

logger = logging.getLogger('django')
# Create your views here.


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


class ProductListView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs):
        error, user = login_auth.auth_validation(request)
        most_popular_product_id, most_popular_product_id_user = validation_user_rating.userdata(
            request)
        product_list = []
        top_rating = []
        product_list_without_rating = []
        top_rating_product_list_data = []
        no_rating_list_data = []
        if user:
            for data in most_popular_product_id_user:
                products = Product.objects.filter(id=data)
                for product in products:
                        top_rating_product_list_data.append({
                            "id": product.id,
                            "name": product.name,
                            "price": product.price,
                            "photo": base64.b64encode(product.photo).decode("utf-8") if product.photo else None,
                            "description": product.description,
                            "date_created": product.manufactured_date,
                        })
            products = Product.objects.all()
            for product in products:
                product_list.append(product.id)
            for data in product_list:
                if data in most_popular_product_id_user:
                    pass
                else:
                    product_list_without_rating.append(data)

            for no_top_rate in product_list_without_rating:
                products = Product.objects.filter(
                    is_void=False, id=no_top_rate)
                for product in products:
                    no_rating_list_data.append({
                        "id": product.id,
                        "name": product.name,
                        "price": product.price,
                        "photo": base64.b64encode(product.photo).decode("utf-8") if product.photo else None,
                        "description": product.description,
                        "date_created": product.manufactured_date,
                    })

        else:
            products = Product.objects.all()
            for product in products:
                product_list.append(product.id)
            for data in product_list:
                if data in most_popular_product_id:
                    top_rating.append(data)
                else:
                    product_list_without_rating.append(data)

        try:
            for top_rate in top_rating:
                products = Product.objects.filter(is_void=False, id=top_rate)
                for product in products:
                    top_rating_product_list_data.append({
                        "id": product.id,
                        "name": product.name,
                        "price": product.price,
                        "photo": base64.b64encode(product.photo).decode("utf-8") if product.photo else None,
                        "description": product.description,
                        "date_created": product.manufactured_date,
                    })
                    pass
            for no_top_rate in product_list_without_rating:
                products = Product.objects.filter(
                    is_void=False, id=no_top_rate)
                for product in products:
                    no_rating_list_data.append({
                        "id": product.id,
                        "name": product.name,
                        "price": product.price,
                        "photo": base64.b64encode(product.photo).decode("utf-8") if product.photo else None,
                        "description": product.description,
                        "date_created": product.manufactured_date,
                    })

            message = {
                globalparamers.RESULT_CODE: globalparamers.SUCCESS_CODE,
                globalparamers.RESULT_DESCRIPTION: globalparamers.SUCCESS_RESULT_DESCRIPTION,
                "data": top_rating_product_list_data,
                "nonRatingList": no_rating_list_data
            }
            return JsonResponse(message, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(str(e), exc_info=True)
            message = {
                globalparamers.RESULT_CODE: globalparamers.UNSUCESS_CODE,
                globalparamers.RESULT_DESCRIPTION: globalparamers.ERROR_MESSAGE
            }
            return JsonResponse(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SubProductListView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            category_id = request.query_params.get("data", None)
            categorys = SubCategory.objects.filter(category=category_id)
            sub_category_list = []
            for category in categorys:
                sub_category_list.append({
                    "id": category.id,
                    "name": category.name
                })
            message = {
                globalparamers.RESULT_CODE: globalparamers.SUCCESS_CODE,
                globalparamers.RESULT_DESCRIPTION: globalparamers.SUCCESS_RESULT_DESCRIPTION,
                "data": sub_category_list
            }
            return JsonResponse(message, status=status.HTTP_200_OK)
        except Exception as e:
            message = custom_exception.custom_exception(request, e)
            return JsonResponse(message, status=status.HTTP_400_BAD_REQUEST)


class ProductFindByIdListView(APIView):
    def get(self, request, pk, *args, **kwargs):

        permission_classes = []
        try:
            product_list = []
            product = Product.objects.get(is_void=False, id=pk)
            product_list = {
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "photo": base64.b64encode(product.photo).decode("utf-8") if product.photo else None,
                "description": product.description,
                "date_created": product.manufactured_date,
            }

            message = {
                globalparamers.RESULT_CODE: globalparamers.SUCCESS_CODE,
                globalparamers.RESULT_DESCRIPTION: globalparamers.SUCCESS_RESULT_DESCRIPTION,
                "data": product_list
            }
            return JsonResponse(message, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(str(e), exc_info=True)
            message = {
                globalparamers.RESULT_CODE: globalparamers.UNSUCESS_CODE,
                globalparamers.RESULT_DESCRIPTION: globalparamers.ERROR_MESSAGE
            }
            return JsonResponse(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class   ProductSearchListView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs):
        search_value = request.query_params.get("data", None)
        if not search_value:
            search_value = ''
        try:
            search_value = int(search_value)
            PRIZE_FLAG = TRUE
        except ValueError:
            search_value = search_value
            PRIZE_FLAG = False

        try:
            product_list = []

            def my_custom_sql(self):
                with connection.cursor() as cursor:
                    if PRIZE_FLAG:
                        query = f"SELECT id, name, price, photo, description FROM Product WHERE price={search_value}"
                    else:
                        query = f"SELECT id, name, price, photo, description FROM Product WHERE name ILIKE '%{search_value}%' or description ILIKE '%{search_value}%' "
                    cursor.execute(query)
                    dict_value = dictfetchall(cursor)
                return dict_value

            products = my_custom_sql(self)
            product_id = []
            for product in products:
                product_id.append(product['id'])
            for product in product_id:
                product = Product.objects.get(id=product)
                product_list.append({
                    "id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "photo": base64.b64encode(product.photo).decode("utf-8") if product.photo else None,
                    "description": product.description,
                    "date_created": product.manufactured_date,
                })

            message = {
                globalparamers.RESULT_CODE: globalparamers.SUCCESS_CODE,
                globalparamers.RESULT_DESCRIPTION: globalparamers.SUCCESS_RESULT_DESCRIPTION,
                "data": product_list
            }
            return JsonResponse(message, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(str(e), exc_info=True)
            message = {
                globalparamers.RESULT_CODE: globalparamers.UNSUCESS_CODE,
                globalparamers.RESULT_DESCRIPTION: globalparamers.ERROR_MESSAGE
            }
            return JsonResponse(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductCommentView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request, pk, *args, **kwargs):

        try:
            data = json.loads(request.body)
            comment = str(data['comment']).strip() if 'comment' in data else ''
            if not comment:
                comment = ''
            product = Order.objects.get(
                is_void=False, customer__id=request.user.id, product__id=pk)
            product.comment = comment
            product.save()
            message = {
                globalparamers.RESULT_CODE: globalparamers.SUCCESS_CODE,
                globalparamers.RESULT_DESCRIPTION: globalparamers.SUCCESS_RESULT_DESCRIPTION,

            }
            return JsonResponse(message, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(str(e), exc_info=True)
            message = {
                globalparamers.RESULT_CODE: globalparamers.UNSUCESS_CODE,
                globalparamers.RESULT_DESCRIPTION: globalparamers.ERROR_MESSAGE
            }
            return JsonResponse(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductRatingView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request, pk, *args, **kwargs):

        try:
            data = json.loads(request.body)
            print('data', data)
            rating = data['rating'] if 'rating' in data else ''
            print('rating', rating)
            product = Order.objects.get(
                product__id=pk, customer__id=request.user)
            product.rating = rating
            product.save()
            message = {
                globalparamers.RESULT_CODE: globalparamers.SUCCESS_CODE,
                globalparamers.RESULT_DESCRIPTION: globalparamers.SUCCESS_RESULT_DESCRIPTION,
            }
            return JsonResponse(message, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            logger.error(str(e), exc_info=True)
            message = {
                globalparamers.RESULT_CODE: globalparamers.UNSUCESS_CODE,
                globalparamers.RESULT_DESCRIPTION: "Product must be Order for give rating."
            }
            return JsonResponse(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            logger.error(str(e), exc_info=True)
            message = {
                globalparamers.RESULT_CODE: globalparamers.UNSUCESS_CODE,
                globalparamers.RESULT_DESCRIPTION: globalparamers.ERROR_MESSAGE
            }
            return JsonResponse(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductOrderAddressChangeListView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        try:
            data1 = request.user
            print('data1', data1)

            user = User.objects.get(id=request.user.id)
            data = {
                "orderLocation": user.order_location
            }
            message = {
                globalparamers.RESULT_CODE: globalparamers.SUCCESS_CODE,
                globalparamers.RESULT_DESCRIPTION: globalparamers.SUCCESS_RESULT_DESCRIPTION,
                "data": data
            }
            return JsonResponse(message, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(str(e), exc_info=True)
            message = {
                globalparamers.RESULT_CODE: globalparamers.UNSUCESS_CODE,
                globalparamers.RESULT_DESCRIPTION: globalparamers.ERROR_MESSAGE
            }
            return JsonResponse(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AddToCardView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):

        try:
            json_error = []
            data = json.loads(request.body)
            product_id = str(data['productId']).strip() if 'productId' in data else ''
            if not product_id:
                json_error.append("Product can not be blank.")
            quantity = str(data['quantity']).strip() if 'quantity' in data else ''
            if not quantity:
                quantity = 0
            if AddToCard.objects.filter(product_id=product_id, customer_id=request.user).exists():
                adds = AddToCard.objects.get(
                    product_id=product_id, customer_id=request.user)
                adds.quantity = quantity
                adds.save()
            else:
                AddToCard.objects.create(product_id=product_id,
                                         customer_id=request.user,
                                         quantity=quantity)
            message = {
                globalparamers.RESULT_CODE: globalparamers.SUCCESS_CODE,
                globalparamers.RESULT_DESCRIPTION: globalparamers.SUCCESS_RESULT_DESCRIPTION,
            }
            return JsonResponse(message, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(str(e), exc_info=True)
            message = {
                globalparamers.RESULT_CODE: globalparamers.UNSUCESS_CODE,
                globalparamers.RESULT_DESCRIPTION: globalparamers.ERROR_MESSAGE
            }
            return JsonResponse(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AddToCardListView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        try:
            add_to_card_list = []
            add_to_cards = AddToCard.objects.filter(customer_id=request.user)
            for add_to_card in add_to_cards:
                product = Product.objects.get(id=add_to_card.product_id)
                add_to_card_list.append({
                    "id": add_to_card.id,
                    "productId": product.id,
                    "nameOfProduct": product.name,
                    "priceOfProduct": product.price,
                    "photo": base64.b64encode(product.photo).decode("utf-8") if product.photo else None,
                    "quantity": add_to_card.quantity
                })
            message = {
                globalparamers.RESULT_CODE: globalparamers.SUCCESS_CODE,
                globalparamers.RESULT_DESCRIPTION: globalparamers.SUCCESS_RESULT_DESCRIPTION,
                "data": add_to_card_list
            }
            return JsonResponse(message, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(str(e), exc_info=True)
            message = {
                globalparamers.RESULT_CODE: globalparamers.UNSUCESS_CODE,
                globalparamers.RESULT_DESCRIPTION: globalparamers.ERROR_MESSAGE
            }
            return JsonResponse(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductPrizeListView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs):
        data = json.loads(request.query_params.get("data", None))
        print('prize data', data)
        low_prize = str(data['lowPrize']).strip() if 'lowPrize' in data else ''
        if not low_prize:
            low_prize = '0'
        high_prize = str(data['highPrize']).strip(
        ) if 'highPrize' in data else ''
        if not high_prize:
            high_prize = '1000'

        print('prize data', data)
        try:
            product_list = []

            def my_custom_sql(self):
                with connection.cursor() as cursor:
                    query = f"SELECT id, name, price, photo, description FROM Product WHERE \
                    price BETWEEN {int(low_prize)} AND {int(high_prize)}"
                    print('query', query)
                    cursor.execute(query)
                    dict_value = dictfetchall(cursor)
                return dict_value
            products = my_custom_sql(self)
            product_id = []
            for product in products:
                product_id.append(product['id'])
            for product in product_id:
                product = Product.objects.get(id=product)
                product_list.append({
                    "id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "photo": base64.b64encode(product.photo).decode("utf-8") if product.photo else None,
                    "description": product.description,
                    "date_created": product.manufactured_date,
                })

            message = {
                globalparamers.RESULT_CODE: globalparamers.SUCCESS_CODE,
                globalparamers.RESULT_DESCRIPTION: globalparamers.SUCCESS_RESULT_DESCRIPTION,
                "data": product_list
            }
            return JsonResponse(message, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(str(e), exc_info=True)
            message = {
                globalparamers.RESULT_CODE: globalparamers.UNSUCESS_CODE,
                globalparamers.RESULT_DESCRIPTION: globalparamers.ERROR_MESSAGE
            }
            return JsonResponse(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AddToCardDeleteView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        try:
            data = json.loads(request.query_params.get("data", None))
            print("delete id", data)
            delete_id = str(data['deleteId']).strip(
            ) if 'deleteId' in data else ''
            print('delete', delete_id, len(delete_id))
            instance = AddToCard.objects.get(id=delete_id)
            instance.delete()
            message = {
                globalparamers.RESULT_CODE: globalparamers.SUCCESS_CODE,
                globalparamers.RESULT_DESCRIPTION: globalparamers.SUCCESS_RESULT_DESCRIPTION,
            }
            return JsonResponse(message, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(str(e), exc_info=True)
            message = {
                globalparamers.RESULT_CODE: globalparamers.UNSUCESS_CODE,
                globalparamers.RESULT_DESCRIPTION: globalparamers.ERROR_MESSAGE
            }
            return JsonResponse(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
