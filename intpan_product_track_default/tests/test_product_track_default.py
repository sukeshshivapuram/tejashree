from odoo.tests.common import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestProductTrackDefault(TransactionCase):

    def test_default_is_storable_template(self):
        """ Test that new product templates have is_storable=True by default """
        product_tmpl = self.env['product.template'].create({
            'name': 'Test Track Default Product Template',
        })
        self.assertTrue(product_tmpl.is_storable, "Product template should have is_storable=True by default")

    def test_explicit_is_storable_false_template(self):
        """ Test that explicit is_storable=False is preserved """
        product_tmpl = self.env['product.template'].create({
            'name': 'Test Non-Storable Product Template',
            'is_storable': False,
        })
        self.assertFalse(product_tmpl.is_storable, "Product template should keep is_storable=False when explicitly set")

    def test_service_product_template(self):
        """ Test that service products have is_storable=False """
        product_tmpl = self.env['product.template'].create({
            'name': 'Test Service Product Template',
            'type': 'service',
        })
        self.assertFalse(product_tmpl.is_storable, "Service product template should have is_storable=False")

    def test_default_is_storable_variant(self):
        """ Test that new product variants have is_storable=True by default """
        product = self.env['product.product'].create({
            'name': 'Test Track Default Product Variant',
        })
        self.assertTrue(product.is_storable, "Product variant should have is_storable=True by default")
