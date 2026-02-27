"""
Test suite for the products app.
Run with:  python manage.py test products --verbosity 2
"""
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Product


def make_user(username='testuser', password='StrongPass123!', email='test@test.com'):
    return User.objects.create_user(username=username, password=password, email=email)

def make_product(owner, **kwargs):
    defaults = {
        'name': 'Toyota Corolla', 'category': 'car', 'brand': 'Toyota',
        'price': '15000.00', 'description': 'Clean car', 'year': 2020,
    }
    defaults.update(kwargs)
    return Product.objects.create(owner=owner, **defaults)

def get_token(client, username='testuser', password='StrongPass123!'):
    res = client.post('/api/token/', {'username': username, 'password': password}, format='json')
    return res.data['access']


class ProductPublicTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = make_user()
        self.product = make_product(self.user)

    def test_anyone_can_list_products(self):
        res = self.client.get('/api/products/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_anyone_can_retrieve_single_product(self):
        res = self.client.get(f'/api/products/{self.product.id}/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_unauthenticated_cannot_create(self):
        res = self.client.post('/api/products/', {'name': 'x', 'category': 'car', 'brand': 'y', 'price': '100', 'year': 2020}, format='json')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class ProductFilterTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = make_user()
        make_product(self.user, name='Toyota Corolla', category='car', brand='Toyota', price='15000', year=2020)
        make_product(self.user, name='Honda Brake Pad', category='spare_part', brand='Honda', price='50', year=None)
        make_product(self.user, name='BMW 3 Series', category='car', brand='BMW', price='35000', year=2022)

    def test_filter_by_category(self):
        res = self.client.get('/api/products/?category=car')
        for item in res.data['results']:
            self.assertEqual(item['category'], 'car')

    def test_search_by_name(self):
        res = self.client.get('/api/products/?search=Corolla')
        self.assertGreater(res.data['count'], 0)

    def test_filter_price_range(self):
        res = self.client.get('/api/products/?min_price=10000&max_price=20000')
        for item in res.data['results']:
            self.assertGreaterEqual(float(item['price']), 10000)
            self.assertLessEqual(float(item['price']), 20000)

    def test_filter_by_brand(self):
        res = self.client.get('/api/products/?brand=toyota')
        for item in res.data['results']:
            self.assertIn('Toyota', item['brand'])

    def test_ordering_price_ascending(self):
        res = self.client.get('/api/products/?ordering=price')
        prices = [float(i['price']) for i in res.data['results']]
        self.assertEqual(prices, sorted(prices))


class ProductCreateTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = make_user()
        token = get_token(self.client)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_create_success(self):
        res = self.client.post('/api/products/', {'name': 'Honda Civic', 'category': 'car', 'brand': 'Honda', 'price': '12000', 'year': 2019}, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['owner'], 'testuser')

    def test_negative_price_rejected(self):
        res = self.client.post('/api/products/', {'name': 'Car', 'category': 'car', 'brand': 'Ford', 'price': '-500', 'year': 2020}, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('price', res.data)

    def test_car_without_year_rejected(self):
        res = self.client.post('/api/products/', {'name': 'Car', 'category': 'car', 'brand': 'Ford', 'price': '5000'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('year', res.data)

    def test_spare_part_without_year_allowed(self):
        res = self.client.post('/api/products/', {'name': 'Brake Pad', 'category': 'spare_part', 'brand': 'Bosch', 'price': '45'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)


class ProductPermissionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.owner = make_user(username='owner', email='owner@test.com')
        self.other = make_user(username='other', email='other@test.com')
        self.product = make_product(self.owner)

    def _login(self, username):
        token = get_token(self.client, username)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_owner_can_update(self):
        self._login('owner')
        res = self.client.put(f'/api/products/{self.product.id}/', {'name': 'Updated', 'category': 'car', 'brand': 'Toyota', 'price': '16000', 'year': 2021}, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_non_owner_cannot_update(self):
        self._login('other')
        res = self.client.put(f'/api/products/{self.product.id}/', {'name': 'Hack', 'category': 'car', 'brand': 'X', 'price': '1', 'year': 2020}, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_can_delete(self):
        self._login('owner')
        res = self.client.delete(f'/api/products/{self.product.id}/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_non_owner_cannot_delete(self):
        self._login('other')
        res = self.client.delete(f'/api/products/{self.product.id}/')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class MyListingsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = make_user()
        make_product(self.user, name='My Car 1')
        make_product(self.user, name='My Car 2')
        other = make_user(username='other2', email='other2@test.com')
        make_product(other, name='Someone Elses Car')

    def test_returns_only_own_products(self):
        token = get_token(self.client)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        res = self.client.get('/api/products/my_listings/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 2)

    def test_unauthenticated_blocked(self):
        res = self.client.get('/api/products/my_listings/')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class UserRegistrationTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_success(self):
        res = self.client.post('/api/users/register/', {'username': 'john', 'email': 'john@test.com', 'password': 'StrongPass123!', 'password_confirm': 'StrongPass123!'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_password_mismatch(self):
        res = self.client.post('/api/users/register/', {'username': 'john', 'email': 'john@test.com', 'password': 'StrongPass123!', 'password_confirm': 'Wrong!'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_email(self):
        make_user(username='u1', email='same@test.com')
        res = self.client.post('/api/users/register/', {'username': 'u2', 'email': 'same@test.com', 'password': 'StrongPass123!', 'password_confirm': 'StrongPass123!'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', res.data)