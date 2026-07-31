# Ajay — Portfolio & Contact Website (Django)

A production-ready, full-stack personal portfolio site built with Django 5 and
Bootstrap 5: Home, About, Skills, and Contact pages, an AJAX contact form
backed by a database, and a customized Django admin dashboard.

## Features

- Responsive Bootstrap 5 UI with a sticky navbar and dark/light mode toggle
  (persisted in `localStorage`)
- Home page hero, quick stats, featured **Projects** section, and CTA
- About page with the full "About Me" content, sectioned into cards
- Skills page with categorized skill cards and animated progress bars
- Contact page with a validated form (Full Name, Email, Phone, Subject,
  Message), submitted via the Fetch API with **no page reload**
- Server-side validation + a hidden honeypot field for basic spam protection
- Contact submissions saved to the database (`Contact` model) and visible in
  the Django admin, with an email notification (console backend in dev)
- Custom admin dashboard showing total / unread messages and project count
- Custom 404 and 500 error pages
- SEO meta tags, scroll animations (AOS), clean URLs, CSRF protection

## Project Structure

```
portfolio_project/
├── manage.py
├── requirements.txt
├── db.sqlite3              (created after migrate)
├── portfolio/               # project settings, urls, wsgi/asgi
├── core/                    # the app: models, views, forms, admin, templates, static
│   ├── models.py            # Contact, Project, Skill
│   ├── views.py             # HomeView, AboutView, SkillsView, ContactView (AJAX)
│   ├── forms.py             # ContactForm (+ honeypot)
│   ├── admin.py / admin_site.py
│   ├── templates/core/      # home, about, skills, contact, base
│   └── static/core/         # css, js, resume placeholder
├── templates/                # 404.html, 500.html, admin/index.html override
└── media/                    # uploaded project images (via admin)
```

## Setup & Run

```bash
# 1. Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Apply database migrations
python manage.py migrate

# 4. Create an admin account
python manage.py createsuperuser

# 5. Run the development server
python manage.py runserver
```

Then visit:
- Site: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

Contact form emails print to the terminal (console email backend) — check
the console after submitting the form.

## Customize

- **Your info & social links**: edit `SITE_NAME`, `OWNER_NAME`,
  `OWNER_TAGLINE`, and `SOCIAL_LINKS` in `portfolio/settings.py`.
- **Resume**: replace the placeholder at
  `core/static/core/resume/Ajay_Resume.pdf` with your real resume (keep the
  same filename, or update the link in `core/templates/core/home.html`).
- **Projects & Skills**: add real entries through the Django admin
  (`/admin/`) — the site automatically falls back to sample/dummy data
  until you add your own rows.
- **Production**: before deploying, set `DJANGO_SECRET_KEY`,
  `DJANGO_DEBUG=False`, and `DJANGO_ALLOWED_HOSTS` as environment
  variables, switch `EMAIL_BACKEND` to a real SMTP backend, and run
  `python manage.py collectstatic`.

## Notes

This project was generated in an environment without internet/package
access, so it has not been run against a live Django install — the code was
hand-written to Django 5.x conventions and syntax-checked, but please run
`python manage.py check` after `pip install`-ing dependencies to catch
anything environment-specific.
