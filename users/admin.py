# # users/admin.py
# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import CustomUser

# class CustomUserAdmin(UserAdmin):
#     model = CustomUser
#     list_display = ['phone_number', 'invitation_code', 'is_staff']
#     fieldsets = (
#         (None, {'fields': ('phone_number', 'password')}),
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
#         # ('Important dates', {'fields': ('last_login', 'date_joined')}),
#         ('Custom fields', {'fields': ('invitation_code',)}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('phone_number', 'password1', 'password2', 'is_staff', 'is_active')}
#         ),
#     )
#     search_fields = ('phone_number',)
#     ordering = ('phone_number',)

# admin.site.register(CustomUser, CustomUserAdmin)

# yourapp/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser

class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    ordering = ['-date_joined']
    list_display = ('phone_number', 'is_active', 'is_staff')
    search_fields = ('phone_number',)
    readonly_fields = ('date_joined',)
    
    # Define the fieldsets for the user detail page
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Personal info', {'fields': ('invitation_code',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('date_joined',)}),
    )
    
    # Define the form for changing user passwords
    add_form_template = 'admin/auth/user/add_form.html'
    change_password_form = None
    add_fieldsets = (
        (None, {
            'fields': ('phone_number', 'password1', 'password2')}
        ),
    )
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            # If editing an existing user, use the password change form
            self.change_password_form = self.get_change_password_form()
        return form

    def get_change_password_form(self):
        from django.contrib.auth.forms import AdminPasswordChangeForm
        return AdminPasswordChangeForm

# Register the CustomUserAdmin with the admin site
admin.site.register(CustomUser, CustomUserAdmin)
