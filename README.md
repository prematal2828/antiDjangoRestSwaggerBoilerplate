# Django DRF Todo API Boilerplate

A production-ready Django REST Framework boilerplate with:
- **Fully custom User model** (email-based, no username field)
- **JWT authentication** (via `djangorestframework-simplejwt`)
- **Token blacklisting** on logout
- **Todo CRUD** with per-user isolation and filtering
- **Auto-generated Swagger UI + ReDoc** (via `drf-spectacular`)

---

## Tech Stack

| Package | Version |
|---|---|
| Django | ≥ 5.0 |
| djangorestframework | ≥ 3.14 |
| drf-spectacular | ≥ 0.27 |
| djangorestframework-simplejwt | ≥ 5.3 |
| django-environ | ≥ 0.11 |
| Pillow | ≥ 10.0 |

---

## Quick Start

### 1. Clone and set up environment
```bash
git clone <your-repo>
cd antiDjangoRestSwaggerBoilerplate

python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Configure environment
```bash
cp .env.example .env
# Edit .env with your SECRET_KEY and any other settings
```

### 3. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create a superuser
```bash
python manage.py createsuperuser
# Enter email + password (no username)
```

### 5. Start development server
```bash
python manage.py runserver
```

---

## API Endpoints

### Documentation
| URL | Description |
|---|---|
| `GET /api/docs/` | **Swagger UI** |
| `GET /api/redoc/` | **ReDoc** |
| `GET /api/schema/` | Raw OpenAPI 3.0 schema (YAML) |

### Auth (`/api/v1/auth/`)
| Method | URL | Auth | Description |
|---|---|---|---|
| `POST` | `register/` | ✗ | Register new user |
| `POST` | `login/` | ✗ | Login → access + refresh tokens |
| `POST` | `token/refresh/` | ✗ | Refresh access token |
| `POST` | `logout/` | ✓ | Blacklist refresh token |
| `GET/PATCH` | `profile/` | ✓ | Get / update own profile |
| `POST` | `password/change/` | ✓ | Change own password |

### Todos (`/api/v1/todos/`)
| Method | URL | Auth | Description |
|---|---|---|---|
| `GET` | `/` | ✓ | List own todos (paginated, filterable) |
| `POST` | `/` | ✓ | Create a todo |
| `GET` | `<id>/` | ✓ | Retrieve a todo |
| `PUT/PATCH` | `<id>/` | ✓ | Update a todo |
| `DELETE` | `<id>/` | ✓ | Delete a todo |

#### Todo query params
- `?search=<term>` — search in title + description
- `?is_completed=true|false` — filter by status
- `?priority=low|medium|high` — filter by priority
- `?ordering=-created_at` — sort results

---

## Project Structure

```
.
├── core/                   # Django project (settings, root URLs, wsgi/asgi)
│   ├── settings.py
│   └── urls.py
├── accounts/               # Custom user app
│   ├── models.py           # AbstractBaseUser + email login
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── todos/                  # Todo app
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── .env.example
├── requirements.txt
└── manage.py
```

---

## Authentication Flow

```
POST /api/v1/auth/login/
→ { "access": "<jwt>", "refresh": "<jwt>" }

# Use in subsequent requests:
Authorization: Bearer <access_token>

# Refresh when access token expires:
POST /api/v1/auth/token/refresh/
→ { "access": "<new_jwt>" }

# Logout (blacklists refresh token):
POST /api/v1/auth/logout/
{ "refresh": "<refresh_token>" }
```

---

## Django Admin
Access at `/admin/` — fully configured for the custom User model.
# antiDjangoRestSwaggerBoilerplate
