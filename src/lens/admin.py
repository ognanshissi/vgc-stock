from django.contrib import admin
from .models import Product, Entry, Exit, Stock, Type


class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ('reference', 'sphere', 'cylindre', 'axe', 'addition', 'in_stock')
    list_filter = (
        ('sphere'),
        ('cylindre'),
        ('axe'),
        ('addition'),
    )


admin.site.register(Product, ProductAdmin)


class EntryAdmin(admin.ModelAdmin):
    model = Entry
    list_display = ('product', 'qty')


admin.site.register(Entry, EntryAdmin)


admin.site.register(Exit)


class StockAdmin(admin.ModelAdmin):
    model = Stock
    list_display = ('product', 'qty')
    list_filter = (
        ('qty'),
    )


admin.site.register(Stock, StockAdmin)
admin.site.register(Type)
