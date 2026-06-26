import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
import django
django.setup()

from django.test import Client

client = Client()
print('login=', client.login(username='superuser', password='superuser123'))
response = client.get('/super/add-furniture/')
print('add_furniture=', response.status_code)
