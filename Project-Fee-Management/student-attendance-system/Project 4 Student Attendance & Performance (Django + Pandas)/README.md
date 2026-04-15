# Student Attendance & Performance Tracker

A Django application for managing student attendance and academic performance. The project uses Django for the web app and Pandas for reporting and analysis.

## Features

- Mark student attendance using a form-based interface
- View a student dashboard with average scores and attendance percentages
- Search students by name on the dashboard
- Export student performance reports as Excel or CSV
- Uses Django admin for adding students, marks, and attendance data

## Project Structure

- `core/` - Django project configuration
- `students/` - main app containing models, views, forms, and templates
- `templates/students/` - HTML templates for dashboard and attendance pages
- `static/` - CSS and static assets
- `db.sqlite3` - SQLite database file

## Requirements

- Python 3.10+ (recommended)
- Django
- pandas
- openpyxl

## Setup

1. Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

2. Install required packages:

```bash
pip install django pandas openpyxl
```

3. Apply database migrations:

```bash
python manage.py migrate
```

4. Create a superuser to access the Django admin:

```bash
python manage.py createsuperuser
```

5. Run the development server:

```bash
python manage.py runserver
```

6. Open the app in your browser:

- Admin: `http://127.0.0.1:8000/admin/`
- App pages: depends on configured URLs (likely `/students/` or `/`)

## Usage

- Add `Student`, `Marks`, and `Attendance` records via Django admin.
- Use the dashboard to analyze student performance and attendance.
- Export reports from the dashboard to Excel or CSV.

## Notes

- The project currently uses SQLite (`db.sqlite3`) by default.
- Keep `DEBUG = False` and set a secure `SECRET_KEY` before deploying to production.
