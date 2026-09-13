from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.components.models import Category, Component

from .models import Supplier, SupplierOffer


class SupplierModelTests(TestCase):
	def setUp(self):
		category = Category.objects.create(name='Resistencias')
		self.component = Component.objects.create(category=category, reference='R1', name='Resistencia 1k')
		self.supplier = Supplier.objects.create(name='Proveedor local')

	def test_supplier_rejects_blank_name(self):
		supplier = Supplier(name='   ')
		with self.assertRaises(ValidationError):
			supplier.full_clean()

	def test_supplier_offer_accepts_decimal_price(self):
		offer = SupplierOffer(
			component=self.component,
			supplier=self.supplier,
			part_number='R-1K',
			price=Decimal('0.1250'),
		)
		offer.full_clean()

	def test_supplier_offer_requires_positive_minimum_quantity(self):
		offer = SupplierOffer(
			component=self.component,
			supplier=self.supplier,
			part_number='R-1K',
			price=Decimal('0.1250'),
			minimum_quantity=0,
		)
		with self.assertRaises(ValidationError):
			offer.full_clean()
