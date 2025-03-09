from django.contrib import admin
from .models import Account, Destination, Log, Role, AccountMember, User
from django.contrib.admin import ModelAdmin



# Account model in Admin site
class Account_admin(admin.ModelAdmin):
    list_display = ['account_name','account_id','created_at','updated_at', 'created_by', 'updated_by']
    search_field = ['account_name','account_id']
    list_filter = ['created_at','updated_at']


# Destination model for Admin site
class Destination_Admin(admin.ModelAdmin):
    list_display = ['account', 'url', 'http_method', 'created_at', 'updated_at', 'created_by', 'updated_by']
    search_fields = ['url', 'http_method']
    list_filter = ['created_at', 'http_method']
 
# Log model for admin site
class Log_Admin(admin.ModelAdmin):
    list_display = ['event_id', 'account', 'destination', 'received_timestamp', 'processed_timestamp', 'status']
    search_fields = ['event_id', 'status']
    list_filter = ['processed_timestamp', 'status']

# AccountMember model for admin site
class Account_MemberAdmin(admin.ModelAdmin):
    list_display = ['account', 'user', 'role', 'created_at', 'updated_at']
    search_fields = ['account__account_name', 'user__email', 'role__role_name']
    list_filter = ['role', 'created_at']

# Role_model for admin site
class Role_Admin(admin.ModelAdmin):
    list_display = ['role_name', 'created_at', 'updated_at']
    search_fields = ['role_name']
    list_filter = ['created_at']

# User model for admin site
class User_Admin(admin.ModelAdmin):
    list_display = ['email', 'created_at', 'updated_at']
    search_fields = ['email']
    list_filter = ['created_at']

# Register the models with the admin site
admin.site.register(Account, Account_admin)
admin.site.register(Destination, Destination_Admin)
admin.site.register(Log, Log_Admin)
admin.site.register(AccountMember, Account_MemberAdmin)
admin.site.register(Role, Role_Admin)
admin.site.register(User, User_Admin)
