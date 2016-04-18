from django.template import Template, Context
from django.test import TestCase
from django.core.paginator import Paginator


class TemplateTagTests(TestCase):

    def test_str2int(self):
        """Test str2int template filter"""
        out = Template(
            "{% load str2int %}"
            "{% if 36 == '36'|str2int %}"
            "it works"
            "{% endif %}"
        ).render(Context({}))

        # check for our addition operation result
        self.assertIn("it works", out)
