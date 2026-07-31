import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(blank=True, max_length=20, validators=[django.core.validators.RegexValidator(message='Enter a valid phone number.', regex='^\\+?[0-9\\s\\-()]{7,20}$')])),
                ('subject', models.CharField(max_length=200)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Contact Message',
                'verbose_name_plural': 'Contact Messages',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('tech_stack', models.CharField(help_text='Comma-separated, e.g. Django, PostgreSQL, React', max_length=250)),
                ('github_url', models.URLField(blank=True)),
                ('live_url', models.URLField(blank=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='projects/')),
                ('order', models.PositiveIntegerField(default=0)),
                ('is_featured', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['order', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('category', models.CharField(choices=[('programming', 'Programming & Problem Solving'), ('web', 'Web Development'), ('backend', 'Backend Development'), ('database', 'Databases'), ('software_eng', 'Software Engineering'), ('testing', 'Testing & Quality'), ('cloud', 'Cloud & DevOps'), ('system_design', 'System Design & Distributed Systems'), ('cs_fundamentals', 'Computer Science Fundamentals'), ('ai', 'AI & Data Technologies')], max_length=30)),
                ('proficiency', models.PositiveIntegerField(default=70, help_text='Proficiency percentage (0-100)')),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ['category', 'order', 'name'],
            },
        ),
    ]
