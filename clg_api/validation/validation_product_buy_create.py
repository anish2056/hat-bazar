import json


def product_buy_validate(request, pk):
    data = json.loads(request.body)
    rating = str(data['rating']).strip() if 'rating' in data else ''
    if not rating:
        rating = 0
    return rating
