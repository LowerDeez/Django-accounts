from django.contrib import admin
from accounts.models import UserProfile, Friend

# Register your models here.
admin.site.empty_value_display = '(None)'


class UserProfileAdmin(admin.ModelAdmin):
    #     Set list_display to control which fields are displayed on the change list page of the admin
    list_display = ('user', 'user_info', 'city', 'website', 'phone', 'view_birth_date', 'role')
    list_filter = ('role', 'city')
    list_editable = ('role', 'city', 'website', 'phone')
    search_fields = ('user__username',)
    #exclude = ('email',)

    def user_info(self, obj):
        return obj.description

    def view_birth_date(self, obj):
        return obj.birth_date

    view_birth_date.empty_value_display = '(None)'
    view_birth_date.short_description = 'Birth date'

    # запрос для сортировки полей
    def get_queryset(self, request):
        queryset = super(UserProfileAdmin, self).get_queryset(request)
        queryset = queryset.order_by('phone', 'user')
        return queryset

admin.site.register(UserProfile, UserProfileAdmin)

admin.site.register(Friend)
