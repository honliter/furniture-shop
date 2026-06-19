import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
import django
django.setup()

from django.test import Client

client = Client()
paths = ['/', '/login/', '/register/', '/cart/', '/checkout/', '/super/add-furniture/']
for path in paths:
    response = client.get(path)
    print(path, response.status_code, response.url if response.status_code in (301, 302) else 'OK')
