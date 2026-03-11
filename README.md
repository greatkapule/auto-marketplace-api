# Auto Marketplace API
A production-ready RESTful API for a **car and spare parts marketplace**, built with Django REST Framework.

# Table of Contents
1. [Features](#features)
2. [Tech Stack](#tech-stack)
3. [Project Structure](#project-structure)
4. [Local Setup](#local-setup)
5. [Environment Variables](#environment-variables)
6. [API Endpoints](#api-endpoints)
7. [Search, Filter & Sort](#search-filter--sort)
8. [Example Requests](#example-requests)
9. [Running Tests](#running-tests)
10. [Deployment — Railway](#deployment--railway)
11. [Deployment — PythonAnywhere](#deployment--pythonanywhere)

## Features

- User registration with password confirmation and email uniqueness check
- JWT login, token refresh, and logout (token blacklisting)
- Full CRUD for car and spare part listings
- Owner-only protection — only the listing owner can edit or delete
- Paginated responses (10 per page)
- Search by name, brand, or description
- Filter by category, brand, price range, year range, and owner username
- Sort by date, price, year, or name
- `/api/products/my_listings/` — see only your own listings
- Production-ready — environment variables, PostgreSQL support, CORS, WhiteNoise

## Tech Stack
| Layer | Technology |
|---|---|
| Framework | Django 6.0 + Django REST Framework |
| Authentication | SimpleJWT (access + refresh tokens) |
| Filtering | django-filter + SearchFilter + OrderingFilter |
| Database | SQLite (dev) / PostgreSQL (production) |
| Static Files | WhiteNoise |
| CORS | django-cors-headers |
| Environment | python-decouple |
| Deployment | Railway / PythonAnywhere |

---

## Project Structure
```
auto-marketplace-api/
├── config/
│   ├── settings.py       # All settings — reads from .env
│   ├── urls.py           # Root URL configuration
│   └── wsgi.py
├── users/
│   ├── serializers.py    # Register + profile serializers with validation
│   ├── views.py          # RegisterView, UserProfileView
│   └── urls.py
├── products/
│   ├── models.py         # Product model
│   ├── serializers.py    # ProductSerializer with full validation
│   ├── views.py          # ProductViewSet + my_listings action
│   ├── filters.py        # Filter by category, brand, price, year, owner
│   ├── permissions.py    # IsOwnerOrReadOnly
│   ├── tests.py          # Full test suite (21 tests)
│   └── urls.py
├── .env.example          # Template — copy to .env and fill in values
├── requirements.txt
├── Procfile              # For Railway deployment
└── runtime.txt           # Pins Python version for deployment
```

## Local Setup
### 1. Clone the repository
```bash
git clone https://github.com/greatkapule/auto-marketplace-api.git
cd auto-marketplace-api
```

### 2. Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
```bash
cp .env.example .env
```
Open `.env` and set at minimum:
```
SECRET_KEY=your-long-random-secret-key
DEBUG=True
```

### 5. Run migrations
```bash
python manage.py migrate
```

### 6. Collect static files
```bash
python manage.py collectstatic --noinput
```

### 7. Create an admin account (optional)
```bash
python manage.py createsuperuser
```

### 8. Start the server
```bash
python manage.py runserver
```

API is live at **http://127.0.0.1:8000/**

---

## Environment Variables
Copy `.env.example` to `.env` and fill in these values:

| Variable | Description | Example |
|---|---|---|
| `SECRET_KEY` | Django secret key (keep secret!) | `abc123xyz...` |
| `DEBUG` | `True` for dev, `False` for production | `True` |
| `ALLOWED_HOSTS` | Comma-separated allowed domains | `127.0.0.1,localhost` |
| `DATABASE_URL` | PostgreSQL URL — leave blank for SQLite | `postgresql://...` |
| `CORS_ALLOWED_ORIGINS` | Allowed frontend origins | `http://localhost:3000` |

Generate a secure secret key:
```bash
python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## API Endpoints
### Authentication

| Method | Endpoint | Description | Access |
|---|---|---|---|
| POST | `/api/token/` | Login — returns access + refresh tokens | Public |
| POST | `/api/token/refresh/` | Get new access token | Public |
| POST | `/api/token/blacklist/` | Logout — invalidates refresh token | Public |

### Users

| Method | Endpoint | Description | Access |
|---|---|---|---|
| POST | `/api/users/register/` | Create a new account | Public |
| GET | `/api/users/profile/` | View profile + listing count | 🔒 Login required |
| PATCH | `/api/users/profile/` | Update your email | 🔒 Login required |

### Products

| Method | Endpoint | Description | Access |
|---|---|---|---|
| GET | `/api/products/` | List all products (paginated) | Public |
| POST | `/api/products/` | Create a listing | 🔒 Login required |
| GET | `/api/products/{id}/` | View one product | Public |
| PUT | `/api/products/{id}/` | Replace a product | 🔑 Owner only |
| PATCH | `/api/products/{id}/` | Partially update | 🔑 Owner only |
| DELETE | `/api/products/{id}/` | Delete a product | 🔑 Owner only |
| GET | `/api/products/my_listings/` | Your own listings | 🔒 Login required |


## Search, Filter & Sort

All parameters work on `GET /api/products/` and can be combined freely.

### Filter Parameters

| Parameter | Example | Description |
|---|---|---|
| `category` | `?category=car` | Filter by `car` or `spare_part` |
| `brand` | `?brand=toyota` | Partial, case-insensitive brand match |
| `owner` | `?owner=john` | All listings by username "john" |
| `min_price` | `?min_price=1000` | Price at least 1000 |
| `max_price` | `?max_price=5000` | Price at most 5000 |
| `min_year` | `?min_year=2018` | Year 2018 or newer |
| `max_year` | `?max_year=2022` | Year 2022 or older |

### Search
`?search=term` — searches across **name**, **brand**, and **description**.

### Ordering
`?ordering=field` — prefix with `-` for descending.

| Value | Result |
|---|---|
| `?ordering=-created_at` | Newest first (default) |
| `?ordering=price` | Cheapest first |
| `?ordering=-price` | Most expensive first |
| `?ordering=-year` | Newest year first |

### Combined example
```
GET /api/products/?category=car&min_year=2018&max_price=20000&ordering=-price
```

## Example Requests
### Register
```bash
curl -X POST http://127.0.0.1:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john",
    "email": "john@example.com",
    "password": "StrongPass123!",
    "password_confirm": "StrongPass123!"
  }'
```

### Login
```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "password": "StrongPass123!"}'
```

### Create a listing
```bash
curl -X POST http://127.0.0.1:8000/api/products/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Toyota Corolla",
    "category": "car",
    "brand": "Toyota",
    "price": "15000.00",
    "description": "Low mileage, excellent condition",
    "year": 2020
  }'
```

### View your own listings
```bash
curl http://127.0.0.1:8000/api/products/my_listings/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Logout
```bash
curl -X POST http://127.0.0.1:8000/api/token/blacklist/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "YOUR_REFRESH_TOKEN"}'
```

---

## Running Tests
```bash
# Run all 21 tests
python manage.py test --verbosity 2

# Run only product tests
python manage.py test products --verbosity 2

# Run only user tests
python manage.py test users --verbosity 2
```

---

## Deployment — Railway

### 1. Push your code to GitHub
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

### 2. Sign up at railway.app
Go to https://railway.app and log in with GitHub.

### 3. Create a new project
Click **New Project → Deploy from GitHub repo** → select `auto-marketplace-api`.

### 4. Add PostgreSQL
Click **+ New → Database → Add PostgreSQL**.
Railway sets `DATABASE_URL` automatically.

### 5. Set environment variables
Go to your service → **Variables** tab and add:

| Variable | Value |
|---|---|
| `SECRET_KEY` | your generated secret key |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `your-app.railway.app` |
| `CORS_ALLOWED_ORIGINS` | `https://your-app.railway.app` |

### 6. Redeploy
Go to **Deployments** tab → click the latest → **Redeploy**.

### 7. Run migrations
Open the Railway terminal and run:
```bash
python manage.py migrate
python manage.py createsuperuser
```

Live API Endpoint: https://auto-marketplace-api-production.up.railway.app/api/

Admin Panel: https://auto-marketplace-api-production.up.railway.app/admin/
---
