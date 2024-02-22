import base64
import logging
import json
from traceback import print_tb
from user.models import User
from clg_api.models import Product, Province, District, Municipality, Category, SubCategory
from. import globalparamers
logger = logging.getLogger('django')


def user_create_register_validation(request, pk):
    json_error = []
    try:
        data = json.loads(request.body)
        username = str(data['username']).strip() if 'username' in data else ''
        if not username:
            json_error.append('Username can not be blank.')
        phone = str(data['phone']).strip() if 'phone' in data else ''
        if not phone:
            json_error.append("Phone number can not blank.")
        else:
            if not phone.isdigit():
                json_error.append("Phone number accept only digits.")
            else:
                pass
        if len(phone) != 10:
            json_error.append("Phone number must 10 digits length only.")
        if pk:
            if User.objects.filter(phone=phone, is_active=True).exclude(id=pk).exists():
                json_error.append("Phone number already exist.")
            else:
                pass
        else:
            if User.objects.filter(phone=phone, is_active=True).exists():
                json_error.append('phone number already exist.')

    except Exception as e:
        logger.error(str(e), exc_info=True)
        json_error.append(globalparamers.ERROR_MESSAGE)


def product_validation(request, pk):
    json_error = []
    try:
        data = json.loads(request.body)
        product_name = str(data['productName']).strip(
        ) if 'productName' in data else ''
        if not product_name:
            json_error.append("Product can not be blank.")
        product = str(data['product']).strip() if 'product' in data else ''
        # if not product:
        #     json_error.append("Product can not be balank.")
        if product:
            if Category.objects.filter(id=product).exists():
                pass
            else:
                json_error.append("Select valid product.")
        sub_product = str(data['subProduct']).strip() if 'subProduct' in data else ''
        # if not sub_product:
        #     json_error.append("Sub product can not be blank.")
        print(222222222222)
        if sub_product :
            print(sub_product)
            if SubCategory.objects.filter(id=sub_product, category=product).exists():
                pass
            else:
                print(999999999999)
                json_error.append("Select valid sub product.")
        print(333333333333333)
        description = str(data['description']) if 'description' in data else ''
        if not description:
            json_error.append("Description can not blank.")

        product_prize = data['productPrize'] if 'productPrize' in data else ''
        if not product_prize:
            json_error.append("Product Prize can not be blank.")

        manufactured_date = str(data['manufacturedDate']).strip(
        ) if 'manufacturedDate' in data else ''
        if not manufactured_date:
            json_error.append("manufactured date prize can not be blank.")
        if manufactured_date:
            manufactured_date = manufactured_date.replace("/", "-")
        photo = data['photo'] if 'photo' in data else ''
        if not photo:
            json_error.append("photo can not be blank.")
        if photo:
            image = photo.split(",")[1]
            image = base64.b64decode(image)
        print(111111111111)
        return json_error, product_name, product, sub_product, description, product_prize, manufactured_date, image
    except Exception as e:
        logger.error(str(e), exc_info=True)
        json_error.append(globalparamers.ERROR_MESSAGE)
        return json_error, None, None, None, None, None, None, None


def vendor_register(request):
    json_error = []
    try:
        data = json.loads(request.body)
        print(data)
        first_name = str(data['firstName']).strip() if 'firstName' else ''
        if not first_name:
            json_error.append("First name can not be blank.")

        last_name = str(data['lastName']).strip() if 'lastName' in data else ''
        if not last_name:
            json_error.append("Last name can not be blank.")

        username = str(data['username']).strip() if 'username' in data else ''
        if not username:
            json_error.append("Username can not be blank.")

        password = data['Password'] if 'Password' in data else ''
        if not password:
            json_error.append("Password can ntot be blank.")

        email = str(data['email']).strip() if 'email' in data else ''
        if not email:
            json_error.append("Email can not be blank.")
        if User.objects.filter(email=email).exists():
            json_error.append('Email already exist.')

        date_of_birth = str(data['dateOfBirth']).strip(
        ) if 'dateOfBirth' in data else ''
        if not date_of_birth:
            json_error.append("Date of birth can ntot be blank.")

        gender = str(data['gender']).strip() if 'gender' in data else ''
        if not gender:
            json_error.append("Gender can ntot be blank.")

        phone = str(data['phone']).strip() if 'phone' in data else ''
        if User.objects.filter(phone=phone).exists():
            json_error.append("Phone number must be unique.")
        if not phone:
            json_error.append("Phone can ntot be blank.")
        toll = str(data['street']).strip() if 'street' in data else ''
        if not toll:
            json_error.append("Toll can not be blank.")
        pan = str(data['pan']).strip() if 'pan' in data else ''
        if not pan:
            json_error.append("Pan number can not be blank.")
        else:
            if User.objects.filter(pan_number=pan).exists():
                json_error.append("Pan number must be unique.")
            else:
                pass

        products = data['product'] if 'product' else ''
        if not products:
            json_error.append("Product can not be blank.")
        else:
            for product in products:
                if Category.objects.filter(id=product).exists():
                    pass
                else:
                    json_error.append("Select valid product.")
                    break
        province = str(data['province']).strip() if 'province' in data else ''
        if province:
            if Province.objects.filter(id=province).exists():
                province = Province.objects.get(id=province)
                province = province.name
            else:
                json_error.append("Select valid Province.")
        else:
            province = ''
        district = str(data['district']).strip() if 'district' in data else ''
        if district:
            if District.objects.filter(id=district).exists():
                district = District.objects.get(id=district)
                district = district.name
            else:
                json_error.append("Select valid district.")
        else:
            district = ''
        municipality = str(data['municipality']).strip(
        ) if 'municipality' in data else ''
        if municipality:
            if Municipality.objects.filter(id=municipality).exists():
                municipality = Municipality.objects.get(id=municipality)
                municipality = municipality.name
            else:
                json_error.append('Select valid municipality.')
        else:
            municipality = ''
        address = province + ' ' + district + ' ' + municipality

        return json_error, first_name, last_name, username, password, email, date_of_birth, gender, phone, toll, address, pan, products
    except Exception as e:
        logger.error(str(e), exc_info=True)
        logger.error(str(e), exc_info=True)
        json_error.append(globalparamers.ERROR_MESSAGE)
        return json_error, None, None, None, None, None, None, None, None, None, None, None, None


def order_validation(request, pk):
    json_error = []
    try:
        data = json.loads(request.body)
        product = str(data['product']).strip() if 'product' in data else ''
        if not product:
            json_error.append("Product can not be balank.")
        else:
            if Product.objects.filter(id=product).exists():
                pass
            else:
                json_error.append("Select valid product.")

        return json_error, product,
    except Exception as e:
        logger.error(str(e), exc_info=True)
        json_error.append(globalparamers.ERROR_MESSAGE)
        return json_error, None


def user_register(request):
    json_error = []
    try:
        data = json.loads(request.body)
        username = str(data['username']).strip() if 'username' in data else ''
        if not username:
            json_error.append("Username can not be blank.")

        password = data['password'] if 'password' in data else ''
        if not password:
            json_error.append("Password can ntot be blank.")

        email = str(data['email']).strip() if 'email' in data else ''
        if not email:
            json_error.append("Email can not be blank.")
        if User.objects.filter(email=email).exists():
            json_error.append('Email already exist.')

        date_of_birth = str(data['dateOfBirth']).strip(
        ) if 'dateOfBirth' in data else ''
        if not date_of_birth:
            json_error.append("Date of birth can not be blank.")

        gender = str(data['gender']).strip() if 'gender' in data else ''
        if not gender:
            json_error.append("Gender can ntot be blank.")

        return json_error, username, password, email, date_of_birth, gender
    except Exception as e:
        logger.error(str(e), exc_info=True)
        json_error.append(globalparamers.ERROR_MESSAGE)
        return json_error, None, None, None, None, None
