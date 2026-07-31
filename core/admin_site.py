from django.contrib.admin import AdminSite


class PortfolioAdminSite(AdminSite):
    site_header = "Ajay Portfolio — Admin"
    site_title = "Ajay Portfolio Admin"
    index_title = "Dashboard"

    def index(self, request, extra_context=None):
        from .models import Contact, Project

        extra_context = extra_context or {}
        extra_context['total_messages'] = Contact.objects.count()
        extra_context['unread_messages'] = Contact.objects.filter(is_read=False).count()
        extra_context['total_projects'] = Project.objects.count()
        return super().index(request, extra_context=extra_context)


admin_site = PortfolioAdminSite(name='portfolioadmin')
