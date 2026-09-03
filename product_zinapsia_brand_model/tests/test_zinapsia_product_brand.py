from odoo.tests.common import TransactionCase
from odoo.tools import mute_logger


class TestZinapsiaProductBrand(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.brand = cls.env["zinapsia.product.brand"].create({"name": "Acme"})

    def test_create_brand_and_assign_to_product(self):
        product = self.env["product.template"].create(
            {
                "name": "Test Product With Brand",
                "zinapsia_brand_id": self.brand.id,
                "zinapsia_model": "X-100",
            }
        )
        self.assertEqual(product.zinapsia_brand_id, self.brand)
        self.assertEqual(product.zinapsia_model, "X-100")

    def test_product_without_brand_or_model(self):
        product = self.env["product.template"].create({"name": "Test Product Without Brand"})
        self.assertFalse(product.zinapsia_brand_id)
        self.assertFalse(product.zinapsia_model)

    def test_search_products_by_brand(self):
        product = self.env["product.template"].create(
            {"name": "Searchable Product", "zinapsia_brand_id": self.brand.id}
        )
        found = self.env["product.template"].search([("zinapsia_brand_id", "=", self.brand.id)])
        self.assertIn(product, found)

    def test_group_products_by_brand(self):
        self.env["product.template"].create(
            {"name": "Grouped Product 1", "zinapsia_brand_id": self.brand.id}
        )
        self.env["product.template"].create(
            {"name": "Grouped Product 2", "zinapsia_brand_id": self.brand.id}
        )
        groups = self.env["product.template"]._read_group(
            [("zinapsia_brand_id", "=", self.brand.id)],
            groupby=["zinapsia_brand_id"],
            aggregates=["__count"],
        )
        self.assertTrue(groups)
        brand, count = groups[0]
        self.assertEqual(brand, self.brand)
        self.assertGreaterEqual(count, 2)

    def test_brand_name_uniqueness(self):
        with mute_logger("odoo.sql_db"), self.assertRaises(Exception):
            with self.env.cr.savepoint():
                self.env["zinapsia.product.brand"].create({"name": "Acme"})

    def test_brand_chatter(self):
        self.assertIn("mail.thread", self.brand._inherit if isinstance(self.brand._inherit, list) else [self.brand._inherit])
        self.assertTrue(hasattr(self.brand, "message_ids"))
        self.brand.message_post(body="Test message")
        self.assertTrue(self.brand.message_ids)
