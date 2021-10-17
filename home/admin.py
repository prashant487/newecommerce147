from django.contrib import admin
from .models import *
from csvexport.actions import csvexport


# Register your models here.
class category(admin.ModelAdmin):
    list_display = ('name', 'slug', 'image')
    search_fields = ['name']
    list_per_page = 20
    actions = [csvexport]


admin.site.register(Categorie, category)
admin.site.register(Slider)
admin.site.register(Ad)
admin.site.register(Brand)


class item(admin.ModelAdmin):
    list_display = ('title', 'price', 'status', 'category', 'brand', 'label', 'image')
    search_fields = ['title', 'description']
    list_filter = ('status', 'label', 'category', 'brand')
    list_per_page = 20
    actions = [csvexport]


admin.site.register(Item, item)
admin.site.register(Cart)
admin.site.register(Contact)
# admin.site.register(Grtotal)







































































