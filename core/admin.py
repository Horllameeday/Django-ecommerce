from django.contrib import admin
from .models import *

# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'ordered',
        'being_delivered',
        'received',
        'payment'
    ]

    list_filter = [
        'ordered',
        'being_delivered',
        'received'
    ]

    search_fields = [
        'user__username',
        'ref_code'
    ]

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
#admin.site.register(Payment)