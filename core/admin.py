from django.contrib import admin
from django.utils.html import format_html

from .admin_site import admin_site
from .models import Contact, Project, Skill


@admin.register(Contact, site=admin_site)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('full_name', 'email', 'subject', 'message')
    readonly_fields = ('full_name', 'email', 'phone', 'subject', 'message', 'created_at')
    ordering = ('-created_at',)
    list_per_page = 25
    actions = ['mark_as_read', 'mark_as_unread']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected messages as read"

    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Mark selected messages as unread"

    def has_add_permission(self, request):
        return False


@admin.register(Project, site=admin_site)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'tech_stack', 'is_featured', 'order', 'preview_image')
    list_editable = ('is_featured', 'order')
    search_fields = ('title', 'tech_stack')
    list_filter = ('is_featured',)

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:40px;border-radius:4px;" />', obj.image.url)
        return "—"
    preview_image.short_description = "Preview"


@admin.register(Skill, site=admin_site)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'proficiency', 'order')
    list_editable = ('proficiency', 'order')
    list_filter = ('category',)
    search_fields = ('name',)
    ordering = ('category', 'order')
