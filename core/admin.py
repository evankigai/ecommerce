from django.contrib import admin


from .models import Item, OrderItem, Order, UserProfile, Kind, Grinch


class AdminItem(admin.ModelAdmin):
    list_display = ['title', 'price', 'kind', 'grinch', 'slug', 'id']

class AdminGrinch(admin.ModelAdmin):
    list_display = ['name', 'id']


class AdminKind(admin.ModelAdmin):
    list_display = ['sign', 'dn']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered'

                    ]
    list_display_links = [
        'user',

    ]
    list_filter = ['ordered'
    ]

    search_fields = [
        'user__username',
        'ref_code'


    ]







admin.site.register(Item, AdminItem)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(UserProfile)
admin.site.register(Kind, AdminKind)
admin.site.register(Grinch, AdminGrinch)
