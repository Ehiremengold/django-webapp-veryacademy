from django.contrib import admin
from .models import Hustle, Category, Comment, Skill
from mptt.admin import MPTTModelAdmin


class SkillAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "timestamp")


admin.site.register(Skill, SkillAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ("name", )


admin.site.register(Category, CategoryAdmin)


class HustleAdmin(admin.ModelAdmin):
    list_display = ('user', 'hustle_name', 'slug', 'category', 'created_on')
    list_filter = ('hustle_name',)
    search_fields = ('hustle_name', 'content', 'category')
    prepopulated_fields = {'slug': ('hustle_name',)}
    raw_id_fields = ('category',)

    class Meta:
        model = Hustle


admin.site.register(Hustle, HustleAdmin)


admin.site.register(Comment, MPTTModelAdmin)
