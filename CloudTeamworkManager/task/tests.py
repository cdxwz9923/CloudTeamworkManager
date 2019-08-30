"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import django
from django.test import TestCase
from .views import create_task, edit_task, delete_task

class testTask(TestCase):
    def setUp(self):
        pass

    def test_create_task(self):
        pass

