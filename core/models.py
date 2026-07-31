from django.core.validators import RegexValidator
from django.db import models

phone_validator = RegexValidator(
    regex=r'^\+?[0-9\s\-()]{7,20}$',
    message="Enter a valid phone number."
)


class Contact(models.Model):
    """A message submitted through the site's Contact form."""

    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20, validators=[phone_validator], blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'

    def __str__(self):
        return f"{self.full_name} — {self.subject}"


class Project(models.Model):
    """A portfolio project shown on the home page."""

    title = models.CharField(max_length=150)
    description = models.TextField()
    tech_stack = models.CharField(max_length=250, help_text="Comma-separated, e.g. Django, PostgreSQL, React")
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

    def tech_list(self):
        return [t.strip() for t in self.tech_stack.split(',') if t.strip()]


class Skill(models.Model):
    """A single skill shown with a progress bar on the Skills page."""

    CATEGORY_CHOICES = [
        ('programming', 'Programming & Problem Solving'),
        ('web', 'Web Development'),
        ('backend', 'Backend Development'),
        ('database', 'Databases'),
        ('software_eng', 'Software Engineering'),
        ('testing', 'Testing & Quality'),
        ('cloud', 'Cloud & DevOps'),
        ('system_design', 'System Design & Distributed Systems'),
        ('cs_fundamentals', 'Computer Science Fundamentals'),
        ('ai', 'AI & Data Technologies'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    proficiency = models.PositiveIntegerField(default=70, help_text="Proficiency percentage (0-100)")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['category', 'order', 'name']

    def __str__(self):
        return f"{self.name} ({self.proficiency}%)"
