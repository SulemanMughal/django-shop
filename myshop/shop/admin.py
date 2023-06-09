from django.contrib import admin
from .models import Category, Product
from parler.admin import TranslatableAdmin

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)


# class CategoryAdmin(TranslatableAdmin):
#     list_display = ['name_trans', 'slug_trans']
#     def get_prepopulated_fields(self, request, obj=None):
#         return {'slug_trans': ('name_trans',)}

# admin.site.register(Category, CategoryAdmin)

class ProductAdmin(TranslatableAdmin):
    list_display = ['name', 'slug', 'price', 'stock',
    'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}

admin.site.register(Product, ProductAdmin)