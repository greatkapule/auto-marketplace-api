# Car & Spare Parts Marketplace API
A RESTful API built with Django REST Framework for a car and spare parts marketplace.
Users can register, authenticate, and manage listings for cars and spare parts.

# Tech Stack
- Python 3
- Django
- Django REST Framework
- SimpleJWT
- django-filter
- SQLite (development)

# Prerequisites
- Python 3.8+
- pip
- Git

# Setup & Installation

# STEP 1 — Clone & Enter Project
```bash
git clone https://github.com/yourusername/auto-marketplace-api.git
cd auto-marketplace-api
```

# STEP 2 — Setup Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

# STEP 3 — Install Dependencies
```bash
pip install -r requirements.txt
```

# STEP 4 — Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

# STEP 5 — Create Superuser
```bash
python manage.py createsuperuser
```

# STEP 6 — Run the Server
```bash
python manage.py runserver
```

Visit: `http://127.0.0.1:8000/`


# Features

- User registration with password validation
- JWT authentication with token refresh
- User profile endpoint
- Full CRUD for car and spare part listings
- Owner-only edit and delete protection
- Search by name, brand, and year of manufacture
- Filter by category, price range, and year range
- Order by date, price, and year
- Public read access for all listings

# API Endpoints

# Authentication & Users
| Method | Endpoint | Description | Access |
|---|---|---|---|
| POST | `/api/users/register/` | Register a new user | Public |
| POST | `/api/token/` | Obtain JWT access token | Public |
| POST | `/api/token/refresh/` | Refresh JWT token | Public |
| GET | `/api/users/profile/` | Get authenticated user profile | Authenticated |

# Products
| Method | Endpoint | Description | Access |
|---|---|---|---|
| GET | `/api/products/` | List all products | Public |
| GET | `/api/products/{id}/` | Retrieve a single product | Public |
| POST | `/api/products/` | Create a new product | Authenticated |
| PUT | `/api/products/{id}/` | Update a product | Owner only |
| DELETE | `/api/products/{id}/` | Delete a product | Owner only |

# Search, Filtering & Ordering
| Query Parameter | Example | Description |
|---|---|---|
| `search` | `?search=toyota` | Search by name, brand or year |
| `category` | `?category=car` | Filter by category |
| `min_price` | `?min_price=1000` | Filter by minimum price |
| `max_price` | `?max_price=5000` | Filter by maximum price |
| `min_year` | `?min_year=2018` | Filter by minimum year |
| `max_year` | `?max_year=2022` | Filter by maximum year |
| `ordering` | `?ordering=-created_at` | Order results (prefix `-` for descending) |


# Example Usage with curl

# Register a user
```bash
curl -X POST http://127.0.0.1:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "edwin", "email": "edwin@email.com", "password": "StrongPass123!"}'
```

# Get JWT token
```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "edwin", "password": "StrongPass123!"}'
```

# Refresh token
```bash
curl -X POST http://127.0.0.1:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "YOUR_REFRESH_TOKEN"}'
```

# View your profile
```bash
curl "http://127.0.0.1:8000/api/users/profile/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

# Create a product
```bash
curl -X POST http://127.0.0.1:8000/api/products/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "name": "Toyota Corolla",
    "category": "car",
    "brand": "Toyota",
    "price": "15000.00",
    "description": "Clean 2020 Toyota Corolla",
    "year": 2020
  }'
```

# Search and filter
```bash
# Search by name, brand or year
curl "http://127.0.0.1:8000/api/products/?search=toyota"
curl "http://127.0.0.1:8000/api/products/?search=2020"

# Filter by category
curl "http://127.0.0.1:8000/api/products/?category=car"

# Filter by price range
curl "http://127.0.0.1:8000/api/products/?min_price=1000&max_price=5000"

# Filter by year range
curl "http://127.0.0.1:8000/api/products/?min_year=2018&max_year=2022"

# Combined filters
curl "http://127.0.0.1:8000/api/products/?category=car&min_year=2018&max_year=2022"

# Order by newest
curl "http://127.0.0.1:8000/api/products/?ordering=-created_at"
```


# Authorization Rules

- Public users can view all products
- Authenticated users can create products
- Only the product owner can update or delete their listing
- Authentication uses JWT Bearer tokens


# Project Structure
```
auto-marketplace-api/
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── users/
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── products/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── permissions.py
│   └── filters.py
├── requirements.txt
└── README.md
```
