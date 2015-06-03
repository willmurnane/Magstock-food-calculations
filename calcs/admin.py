from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(Unit)
admin.site.register(PurchaseableItem)
admin.site.register(Meal)
admin.site.register(MealComponent)
