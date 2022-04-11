from django.urls import reverse, resolve
from django.test import SimpleTestCase
from ..views import UserSerializerView
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import get_user_model



User = get_user_model

class ApiUrlsTests(SimpleTestCase):
    
    def test_get_customers_is_resolved(self):
        url = reverse('sign_up')
        self.assertEquals(resolve(url).func.view_class, UserSerializerView)
  