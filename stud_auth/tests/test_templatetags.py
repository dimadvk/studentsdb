from django.test import TestCase
from django.template import Template, Context


class TestTemplatetags(TestCase):

    def test_assign_variable(self):
        # check if both variables exists
        html = Template(
            "{% load assign_variable %}"
            "{% assign_variable var1 var2 as var %}"
            "{% if var == var1 %}"
            " it works " 
            "{% endif %}").render(Context({'var1':'x', 'var2':'x'}))
        self.assertIn('it works', html)
        # check if only second variable exists
        html = Template(
            "{% load assign_variable %}"
            "{% assign_variable var1 var2 as var %}"
            "{% if var == var2 %}"
            " it works " 
            "{% endif %}").render(Context({'var2':'x'}))
        self.assertIn('it works', html)
