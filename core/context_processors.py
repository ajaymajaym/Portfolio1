from django.conf import settings


def site_meta(request):
    """Makes site-wide info (owner name, tagline, social links) available in every template."""
    return {
        'SITE_NAME': settings.SITE_NAME,
        'OWNER_NAME': settings.OWNER_NAME,
        'OWNER_TAGLINE': settings.OWNER_TAGLINE,
        'SOCIAL_LINKS': settings.SOCIAL_LINKS,
    }
