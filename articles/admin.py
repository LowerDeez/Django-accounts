from django.contrib import admin
from .models import Article


# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'create_user', 'slug', 'status', 'create_date', 'update_date']
    list_filter = ['create_user', 'status', 'create_date', 'update_date']
    list_editable = ['status']
    prepopulated_fields = {'slug': ('title', )}

admin.site.register(Article, ArticleAdmin)