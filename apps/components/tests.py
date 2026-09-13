from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import Category, Component, Specification


class ComponentModelTests(TestCase):
	def setUp(self):
		self.category = Category.objects.create(name='Circuitos integrados')

	def test_category_generates_slug(self):
		self.assertEqual(self.category.slug, 'circuitos-integrados')

	def test_component_rejects_blank_name(self):
		component = Component(category=self.category, reference='U1', name='   ')
		with self.assertRaises(ValidationError):
			component.full_clean()

	def test_specification_requires_attribute_and_value(self):
		specification = Specification(
			component=Component.objects.create(category=self.category, reference='U1', name='Temporizador'),
			attribute=' ',
			value='',
		)
		with self.assertRaises(ValidationError) as context:
			specification.full_clean()
		self.assertIn('attribute', context.exception.message_dict)
		self.assertIn('value', context.exception.message_dict)
