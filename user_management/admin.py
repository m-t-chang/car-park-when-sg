from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account


class AccountAdmin(UserAdmin):
    list_display = ('email', 'name', 'surname', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'name', 'surname')
    readonly_fields = ('id', 'date_joined', 'last_login')

    # django requires this stuff to be there
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'name', 'surname', 'date_joined', 'last_login')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff')})
    )

    add_fieldsets = (
        (None, {'classes': ('wide',),  # this classes - wide line just adds more spacing on the form
                'fields': ('email', 'name', 'surname', 'password1', 'password2'),
                }),
    )


admin.site.register(Account, AccountAdmin)
