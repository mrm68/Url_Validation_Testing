from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User
from base.models import Item
"""
this module is going to test the following cases:

# GET DATA SUCCESS
    def test_getData_success(self):
    
# GET DATA UNAUTHENTICATED
    def test_getData_unauthenticated(self):
    
# GET DATA NO ITEMS
    def test_getData_no_items(self):
    
# ADD ITEM SUCCESS
    def test_addItem_success(self):
    
# ADD ITEM UNAUTHENTICATED
    def test_addItem_unauthenticated(self):
    
# ADD INVALID ITEM
    def test_addItem_invalid_data(self):
"""

class ApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username="testuser", password="testpassword")
        self.client.force_authenticate(self.user)

    # GET DATA SUCCESS
    def test_getData_success(self):
        # Create some test items
        Item.objects.create(name="Test Item 1")
        Item.objects.create(name="Test Item 2")

        response = self.client.get(reverse("get_data"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    # GET DATA UNAUTHENTICATED
    def test_getData_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse("get_data"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # GET DATA NO ITEMS
    def test_getData_no_items(self):
        response = self.client.get(reverse("get_data"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    # ADD ITEM SUCCESS
    def test_addItem_success(self):
        data = {"name": "New Item"}
        response = self.client.post(reverse("add_item"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "New Item")

    # ADD ITEM UNAUTHENTICATED
    def test_addItem_unauthenticated(self):
        self.client.force_authenticate(user=None)
        data = {"name": "New Item"}
        response = self.client.post(reverse("add_item"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ADD INVALID ITEM
    def test_addItem_invalid_data(self):
        data = {"name":""}
        response = self.client.post(reverse("add_item"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
