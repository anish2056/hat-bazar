from clg_api.models import Product, Order
import json
from datetime import datetime
from rest_framework.decorators import APIView
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from django.http import JsonResponse
import base64
from clg_api import globalparamers
import logging
import pandas as pd
import matplotlib.pyplot as plt
import base64
import io
import numpy as np


def barGraph(request, start_date, end_date, com_end_date):
    print("*********", request.user)
    print(start_date, end_date, 'date')
    quantity = []
    product_name = []
    old_users = Order.objects.filter(
        vendor_id__id=request.user, creaed_at__range=(start_date, end_date))

    print('2222222222222222222222222222222222222222', old_users)
    for old_user in old_users:
        product = Product.objects.get(id=old_user.product)
        product_name.append(product.name)
        quantity.append(old_user.quantity)
    print('quantity', quantity)
    print("prduct_name", product_name)
    dict = {
        "product": product_name,
        "quantity": quantity
    }
    df = pd.DataFrame(dict)
    bargraphlist = pd.DataFrame(df.groupby('product')['quantity'].sum())
    df1 = bargraphlist.reset_index()
    quantity1 = df1['quantity'].tolist()
    product1 = df1['product'].tolist()
    print('quantity', quantity1)
    print("prduct_name", product1)

    plt.switch_backend('AGG')
    plt.bar(product1, quantity1, width=0.3, color='green')
    plt.xlabel('Product name')
    plt.ylabel('total sales')
    plt.title('report')
    for i in range(len(quantity1)):
        plt.text(i, quantity1[i], quantity1[i], ha="center", va="bottom")
    plt.tight_layout()
    graph = get_graph(request)
    graph1 = pieChart(request, start_date, end_date, com_end_date)

    return graph, graph1


def barGraph1(request, start_date, end_date):
    print("*********", request.user)
    print(start_date, end_date, 'date')
    quantity = []
    product_name = []
    old_users = Order.objects.filter(
        vendor_id__id=request.user, creaed_at__range=(start_date, end_date))

    print('2222222222222222222222222222222222222222', old_users)
    for old_user in old_users:
        product = Product.objects.get(id=old_user.product)
        product_name.append(product.name)
        quantity.append(old_user.quantity)
    print('quantity', quantity)
    print("prduct_name", product_name)
    dict = {
        "product": product_name,
        "quantity": quantity
    }
    df = pd.DataFrame(dict)
    bargraphlist = pd.DataFrame(df.groupby('product')['quantity'].sum())
    df1 = bargraphlist.reset_index()
    quantity2 = df1['quantity'].tolist()
    product2 = df1['product'].tolist()

    plt.switch_backend('AGG')
    plt.bar(product2, quantity2, width=0.3, color='red')
    plt.xlabel('Product name')
    plt.ylabel('total sales')
    plt.title('report')
    plt.tight_layout()
    graph2 = get_graph2(request)
    return graph2


def pieChart(request, start_date, end_date, com_end_date):
    quantity9 = []
    product_name9 = []
    if com_end_date is None:
        old_users = Order.objects.filter(
            vendor_id__id=request.user, creaed_at__range=(start_date, end_date))

    else:
        old_users = Order.objects.filter(
            vendor_id__id=request.user, creaed_at__range=(start_date, com_end_date))

    print('2222222222222222222222222222222222222222', old_users)
    for old_user in old_users:
        product = Product.objects.get(id=old_user.product)
        product_name9.append(product.name)
        quantity9.append(old_user.quantity)
    print('quantity', quantity9)
    print("prduct_name", product_name9)
    dict = {
        "product": product_name9,
        "quantity": quantity9
    }
    df = pd.DataFrame(dict)
    bargraphlist = pd.DataFrame(df.groupby('product')['quantity'].sum())
    df1 = bargraphlist.reset_index()
    quantity1 = df1['quantity'].tolist()
    product1 = df1['product'].tolist()
    print('quantity', quantity1)
    print("prduct_name", product1)
    len1 = len(quantity1)
    List = [0] * len1
    b = quantity1.index(max(quantity1))
    List[b] = 0.08
    y = np.array(quantity1)

    myexplode = List
    plt.switch_backend('AGG')
    plt.pie(y, labels=product1, radius=1,
            autopct='%.3f%%', explode=myexplode, shadow=True)
    plt.title('pie-chart')
    plt.legend(title='Product Category')
    for i in range(len(quantity1)):
        plt.text(i, quantity1[i], quantity1[i], ha="center", va="bottom")
    plt.tight_layout()
    graph = get_graph1(request)
    return graph


def get_graph2(request):
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()

    return graph


def get_graph(request):
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()

    return graph


def get_graph1(request):
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph1 = graph.decode('utf-8')
    buffer.close()

    return graph1


logger = logging.getLogger('django')
#  Create your views here.


class ProducMatplotView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):

        try:
            graph2 = None
            com_end_date = None
            data = json.loads(request.query_params.get("data", None))
            print("data", data)
            start_date = str(data['stardDate']).strip(
            ) if 'stardDate' in data else ''
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()

            end_date = str(data['endDate']).strip() if 'endDate' in data else ''
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

            is_compare = str(data['compare']).strip(
            ) if 'compare' in data else ''
            if str(is_compare) == str(True):
                com_start_date = str(data['comStardDate']).strip(
                ) if 'comStardDate' in data else ''
                com_start_date = datetime.strptime(
                    com_start_date, '%Y-%m-%d').date()

                com_end_date = str(data['comEndDate']).strip(
                ) if 'comEndDate' in data else ''
                com_end_date = datetime.strptime(
                    com_end_date, '%Y-%m-%d').date()

                graph2 = barGraph1(request, com_start_date, com_end_date)
            # print(start_date,end_date, com_start_date, com_end_date,111111111111111)
            # start_date = '2022-08-22'
            # end_date = '2022-09-25'

            graph, graph1 = barGraph(
                request, start_date, end_date, com_end_date)

            print('request user', request.user)
            pass
            message = {
                globalparamers.RESULT_CODE: globalparamers.SUCCESS_CODE,
                globalparamers.RESULT_DESCRIPTION: globalparamers.SUCCESS_RESULT_DESCRIPTION,
                "data": {"graph": graph,
                         "graph1": graph1,
                         "graph2": graph2}
            }
            return JsonResponse(message, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(str(e), exc_info=True)
            message = {
                globalparamers.RESULT_CODE: globalparamers.UNSUCESS_CODE,
                globalparamers.RESULT_DESCRIPTION: globalparamers.ERROR_MESSAGE
            }
            return JsonResponse(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
