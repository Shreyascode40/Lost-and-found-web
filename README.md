# Lost & Found Web Application

A Django-based web application for managing lost and found items within educational institutions.

## Features

- **User Authentication** - Students can register and login
- **Item Management** - Admins can add lost/found items
- **Claim System** - Users can claim found items
- **Admin Dashboard** - Institution admins can manage claims
- **Multi-institution Support** - Multiple institutions can use the platform

## Tech Stack

- **Backend**: Django 5.2
- **Database**: PostgreSQL (default) / SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Icons**: Font Awesome

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Shreyascode40/Lost-and-found-web.git
cd Lost-and-found-web
```

2. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install django psycopg2-binary
```

4. Configure database (PostgreSQL):
```python
# In lostfound_project/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'lostfound_db',
        'USER': 'your_postgres_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Run the server:
```bash
python manage.py runserver
```

## Usage

1. **Admin Registration**: Visit `/institution/register/` to register your institution
2. **Admin Login**: Visit `/admin_panel/login/` to access admin dashboard
3. **User Registration**: Visit `/accounts/register/` to create user accounts
4. **Add Items**: Login as admin and use the "Add Item" option
5. **Claim Items**: Users can claim found items from the home page

## Project Structure

```
lostfound_project/
├── accounts/          # User authentication
├── admin_panel/       # Admin dashboard
├── claim/            # Claim system
├── institution/      # Institution management
├── items/            # Item management
├── lostfound_project/ # Django project settings
├── static/           # Static files (CSS, JS, images)
└── templates/        # HTML templates
```

## License

MIT License


## Author
Shreyas More