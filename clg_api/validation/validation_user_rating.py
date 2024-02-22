from clg_api.models import Order
import pandas as pd
from clg_api.login_auth import auth_validation


# Create your views here.
def userdata(request):
    datas = Order.objects.all()

    productId = []
    userId = []
    rating = []
    for a in datas:
        productId.append(a.product.id)
        userId.append(a.customer.id)
        rating.append(a.rating)

    dict = {
        "productId": productId,
        "userId": userId,
        "rating": rating

    }

    global df
    df = pd.DataFrame(dict)

    popular_products = pd.DataFrame(df.groupby('productId')['rating'].count())
    most_popular = popular_products.sort_values('rating', ascending=False)

    df1 = most_popular.reset_index()
    df1 = df1.sort_values('rating', ascending=False)
    most_popular_product_id = df1['productId'].tolist()
    userRatings = df.pivot_table(index=['userId'], columns=[
                                 'productId'], values='rating')
    print("useRating", userRatings)

    userRatings = userRatings.fillna(0)
    print(userRatings)

    corrMatrix = userRatings.corr(method='pearson')
    print('correlation')
    print(corrMatrix)

    def get_similar(productId, rating):
        similar_ratings = corrMatrix[productId]*(rating-2)
        similar_ratings = similar_ratings.sort_values(ascending=False)
        print((similar_ratings))
        return similar_ratings

   # old_user = [(102, 4), (112, 4), (312, 3)]
    most_popular_product_id_user = None
    eroor, user = auth_validation(request)
    print('user', user)
    if user:
        old_user = Order.objects.filter(
            customer__id=user).values_list('product', 'rating')
        print('1111111111111111111111111111111111111111111', old_user)
        if Order.objects.filter(customer__id=user).exists():
            l1 = []
            for i in old_user:
                l1.append(i)
            print('l1 ', l1)
            similar_product = pd.DataFrame()
            for productId, rating in l1:
                similar_product = similar_product.append(
                    get_similar(productId, rating), ignore_index=True)
            ssss = similar_product.sum().sort_values(ascending=False)
            print(ssss)
            df2 = ssss.reset_index()
            print("#########", type(df2))

            most_popular_product_id_user = df2['productId'].tolist()
            print("list", most_popular_product_id_user)
        else:
            most_popular_product_id_user = most_popular_product_id
    return most_popular_product_id, most_popular_product_id_user
