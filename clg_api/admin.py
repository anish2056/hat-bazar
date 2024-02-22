from django.contrib import admin
from . models import Order, Product, Province, District, Category, SubCategory

# Register your models here.
admin.site.register(Province)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(District)
admin.site.register(Category)
admin.site.register(SubCategory)
