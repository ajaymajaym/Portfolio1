from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from .forms import ContactForm
from .models import Project, Skill


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"{settings.OWNER_NAME} — Home"
        context['meta_description'] = (
            "Portfolio of Ajay, an aspiring Software Engineer specializing in full-stack "
            "development, system design, and cloud technologies."
        )
        projects = Project.objects.filter(is_featured=True)
        context['projects'] = projects if projects.exists() else DUMMY_PROJECTS
        return context


class AboutView(TemplateView):
    template_name = 'core/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"About {settings.OWNER_NAME}"
        context['meta_description'] = (
            "Learn about Ajay's journey as an aspiring software engineer — from programming "
            "fundamentals to system design, cloud computing, and AI."
        )
        return context


class SkillsView(TemplateView):
    template_name = 'core/skills.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Skills — {settings.OWNER_NAME}"
        context['meta_description'] = "Technical and professional skills of Ajay, Software Engineer."

        skills = Skill.objects.all()
        if skills.exists():
            grouped = {}
            for skill in skills:
                grouped.setdefault(skill.get_category_display(), []).append(skill)
            context['skill_groups'] = grouped
        else:
            context['skill_groups'] = DUMMY_SKILLS
        return context


class ContactView(View):
    """Renders the contact page and handles AJAX (fetch) form submissions."""

    template_name = 'core/contact.html'

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {
            'form': form,
            'page_title': f"Contact {settings.OWNER_NAME}",
            'meta_description': "Get in touch with Ajay for opportunities, collaboration, or questions.",
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

        if form.is_valid():
            if form.is_spam():
                # Silently "succeed" for bots so they don't learn the honeypot exists.
                if is_ajax:
                    return JsonResponse({'success': True, 'message': 'Thank you! Your message has been sent.'})
                return render(request, self.template_name, {'form': ContactForm(), 'sent': True})

            contact = form.save()
           

            if is_ajax:
                return JsonResponse({
                    'success': True,
                    'message': f"Thanks {contact.full_name.split()[0]}! Your message has been sent successfully.",
                })
            return render(request, self.template_name, {'form': ContactForm(), 'sent': True})

        if is_ajax:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        return render(request, self.template_name, {'form': form})

    def _send_notification(self, contact):
        try:
            send_mail(
                subject=f"New portfolio contact: {contact.subject}",
                message=(
                    f"From: {contact.full_name} <{contact.email}>\n"
                    f"Phone: {contact.phone or 'N/A'}\n\n"
                    f"{contact.message}"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_NOTIFICATION_EMAIL],
                fail_silently=True,
            )
        except Exception:
            # Never let an email failure break the user-facing form submission.
            pass


def custom_404(request, exception=None):
    return render(request, '404.html', status=404)


def custom_500(request):
    return render(request, '500.html', status=500)


# ---------------------------------------------------------------------------
# Dummy fallback content — shown automatically until real Project/Skill rows
# are added through the Django admin, so the site never looks empty.
# ---------------------------------------------------------------------------

class _DummyProject:
    def __init__(self, title, description, tech_stack, github_url='#', live_url='#'):
        self.title = title
        self.description = description
        self.tech_stack = tech_stack
        self.github_url = github_url
        self.live_url = live_url
        self.image = None

    def tech_list(self):
        return [t.strip() for t in self.tech_stack.split(',')]


DUMMY_PROJECTS = [
    _DummyProject(
        "Task Manager API",
        "A RESTful task-management backend with JWT authentication, role-based access "
        "control, and full CRUD for tasks and projects.",
        "Django, Django REST Framework, PostgreSQL, JWT",
    ),
    _DummyProject(
        "E-Commerce Storefront",
        "A full-stack e-commerce app with a product catalog, cart, and a checkout flow "
        "backed by a mock payment gateway.",
        "Django, React, PostgreSQL, Docker",
    ),
    _DummyProject(
        "Real-Time Chat App",
        "A WebSocket-based chat application supporting multiple rooms, message history, "
        "and typing indicators.",
        "Django Channels, Redis, JavaScript",
    ),
    _DummyProject(
        "CI/CD Pipeline Demo",
        "A sample pipeline that lints, tests, and deploys a containerized app automatically "
        "on every push.",
        "GitHub Actions, Docker, AWS, Kubernetes",
    ),
]

DUMMY_SKILLS = {
    'Programming & Problem Solving': [
        {'name': 'Python', 'proficiency': 85}, {'name': 'Java', 'proficiency': 75},
        {'name': 'C/C++', 'proficiency': 65}, {'name': 'Data Structures & Algorithms', 'proficiency': 80},
    ],
    'Web Development': [
        {'name': 'HTML/CSS/JavaScript', 'proficiency': 85}, {'name': 'TypeScript', 'proficiency': 65},
        {'name': 'React', 'proficiency': 70}, {'name': 'REST APIs', 'proficiency': 80},
    ],
    'Backend Development': [
        {'name': 'Django', 'proficiency': 85}, {'name': 'Flask / FastAPI', 'proficiency': 70},
        {'name': 'Spring Boot', 'proficiency': 55},
    ],
    'Databases': [
        {'name': 'SQL / PostgreSQL', 'proficiency': 80}, {'name': 'MongoDB', 'proficiency': 65},
        {'name': 'Redis', 'proficiency': 55},
    ],
    'Cloud & DevOps': [
        {'name': 'Docker', 'proficiency': 70}, {'name': 'AWS', 'proficiency': 60},
        {'name': 'Kubernetes', 'proficiency': 50}, {'name': 'CI/CD (GitHub Actions)', 'proficiency': 65},
    ],
    'System Design': [
        {'name': 'High/Low-Level Design', 'proficiency': 65}, {'name': 'Scalability & Caching', 'proficiency': 60},
        {'name': 'Distributed Systems', 'proficiency': 55},
    ],
    'AI & Data': [
        {'name': 'NumPy / Pandas', 'proficiency': 75}, {'name': 'Machine Learning', 'proficiency': 60},
        {'name': 'Generative AI / LLM APIs', 'proficiency': 70},
    ],
}
