from django.template import Template, Context
from django.test import TestCase
from django.core.paginator import Paginator
from django.contrib.auth.models import User


class TemplateTagTests(TestCase):

    def test_str2int(self):
        """Test str2int template filter"""
        # try correct value
        out = Template(
            "{% load str2int %}"
            "{% if 36 == '36'|str2int %}"
            "it works"
            "{% endif %}"
        ).render(Context({}))
        # check for our addition operation result
        self.assertIn("it works", out)

        # try incorrect value
        out = Template(
            "{% load str2int %}"
            "{% if 0 == 'x'|str2int %}"
            "it works"
            "{% endif %}"
        ).render(Context({}))
        # check for our addition operation result
        self.assertIn("it works", out)

    def test_nice_username(self):
        """Test nice_username template filter"""
        user = User(username='test_user')
        # try user without full name
        out = Template(
            "{% load nice_username %}"
            "{% if 'test_user' == user|nice_username %}"
            "it works"
            "{% endif %}"
        ).render(Context({'user':user}))
        # check for our addition operation result
        self.assertIn("it works", out)

        user.first_name, user.last_name = 'f_name', 'l_name'
        # try user without full name
        out = Template(
            "{% load nice_username %}"
            "{% if 'f_name l_name' == user|nice_username %}"
            "it works"
            "{% endif %}"
        ).render(Context({'user':user}))
        # check for our addition operation result
        self.assertIn("it works", out)

