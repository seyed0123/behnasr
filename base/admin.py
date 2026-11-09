from django.contrib import admin
from .models import *

# Register your models here.
# Customizing the Company admin interface
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'slogan', 'phone', 'email', 'language')  # Display these fields in the list view
    search_fields = ('name', 'slogan', 'address', 'phone', 'email')  # Add search functionality
    list_filter = ('language',)  # Add filtering by language

# Customizing the Category admin interface
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'language')
    list_filter = ('language',)
    search_fields = ('title',)

# Customizing the About_item admin interface
class AboutItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'language', 'order')  # Add 'order' for sorting
    search_fields = ('title', 'text')
    list_filter = ('language',)

# Customizing the Customer admin interface
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Display customer name
    search_fields = ('name',)

# Customizing the Service admin interface
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'language', 'order', 'hidden')  # Show more details in the list view
    search_fields = ('title', 'description')
    list_filter = ('language', 'hidden')

# Customizing the Product admin interface
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'language', 'order', 'hidden')  # Use category_title method here
    search_fields = ('title', 'short_description', 'description')
    list_filter = ('language', 'category', 'hidden')

# Customizing the Member admin interface
class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'language', 'order', 'hidden')
    search_fields = ('name', 'position')
    list_filter = ('language', 'hidden')

# Customizing the Pricing admin interface
class PricingAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'language', 'order')
    search_fields = ('title', 'description')
    list_filter = ('language',)

# Customizing the Information admin interface
class InformationAdmin(admin.ModelAdmin):
    list_display = ('title', 'language', 'order')
    search_fields = ('title', 'description')
    list_filter = ('language',)

# Registering the models with their custom admin classes
admin.site.register(Company, CompanyAdmin)
admin.site.register(About_item, AboutItemAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Pricing, PricingAdmin)
admin.site.register(Information, InformationAdmin)
admin.site.register(Category, CategoryAdmin)
