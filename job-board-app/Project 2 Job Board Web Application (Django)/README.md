# Job Board Web Application (Django)

A Django-based job board web application with support for user accounts, employer dashboards, job posting, and job applications.

## Project Structure

- `accounts/` - custom user model, signup/login flows, authentication views and forms.
- `jobs/` - job listings, application workflows, employer dashboard, and job management.
- `core/` - Django project settings, URL configuration, and WSGI/ASGI entry points.
- `templates/` - shared base templates and registration templates.
- `static/` - static assets like CSS, JavaScript, and images.
- `db.sqlite3` - SQLite database file used for local development.

## Features

- Custom user model in `accounts.User`
- Signup and login functionality
- Job posting and detail pages
- Job application process
- Employer dashboard for managing jobs and applications

## Setup

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install Django:

```powershell
pip install django
```

3. Apply database migrations:

```powershell
python manage.py migrate
```

4. Create a superuser (optional):

```powershell
python manage.py createsuperuser
```

## Run the Development Server

```powershell
python manage.py runserver
```

Open your browser at `http://127.0.0.1:8000/`.

## Notes

- The project uses SQLite for local development.
- Static files are served from the `static/` directory.
- Default authentication redirect URLs are configured in `core/settings.py`.

## Recommended Improvements

- Add a `requirements.txt` file to pin dependencies.
- Add `README` sections for environment-specific deployment.
- Configure email backend for production use.
