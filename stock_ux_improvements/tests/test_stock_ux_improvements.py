from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged

from .. import uninstall_hook


@tagged("post_install", "-at_install")
class TestStockUxImprovements(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.vendor = cls.env["res.partner"].create({"name": "Test vendor"})
        cls.customer = cls.env["res.partner"].create({"name": "Test customer"})
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test storable product",
                "is_storable": True,
                "purchase_method": "purchase",
            }
        )
        cls.stock_location = cls.env.ref("stock.stock_location_stock")
        cls.customer_location = cls.env.ref("stock.stock_location_customers")
        cls.picking_type_out = cls.env.ref("stock.picking_type_out")

    def _confirm_and_receive_po(self, qty):
        order = self.env["purchase.order"].create(
            {
                "partner_id": self.vendor.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product.id,
                            "product_qty": qty,
                            "price_unit": 10.0,
                        },
                    )
                ],
            }
        )
        order.button_confirm()
        self._validate(order.picking_ids)
        return order

    def _validate(self, picking):
        picking.action_assign()
        for move in picking.move_ids:
            move.quantity = move.product_uom_qty
        picking.move_ids.picked = True
        picking.button_validate()

    def _return_wizard(self, picking, qty):
        wizard = (
            self.env["stock.return.picking"]
            .with_context(active_id=picking.id, active_ids=picking.ids, active_model="stock.picking")
            .create({})
        )
        wizard.product_return_moves.quantity = qty
        return wizard

    def _exchange(self, order, qty):
        receipt = order.picking_ids
        action = self._return_wizard(receipt, qty).action_create_exchanges()
        return_picking = self.env["stock.picking"].browse(action["res_id"])
        exchange_picking = self.env["stock.picking"].search([("return_id", "=", return_picking.id)])
        return return_picking, exchange_picking

    # Return wizard view and exchanges (formerly sale_stock_ux_return_correction)

    def test_adhoc_view_deactivated(self):
        adhoc_view = self.env.ref("sale_stock_ux.view_stock_return_picking_form")
        self.assertFalse(adhoc_view.active)

    def test_incoming_exchange_allowed_even_when_marked_to_refund(self):
        order = self._confirm_and_receive_po(2)
        wizard = self._return_wizard(order.picking_ids, 2)
        self.assertTrue(all(wizard.product_return_moves.mapped("to_refund")))

        action = wizard.action_create_exchanges()

        return_picking = self.env["stock.picking"].browse(action["res_id"])
        exchange_picking = self.env["stock.picking"].search([("return_id", "=", return_picking.id)])
        self.assertTrue(exchange_picking, "The native exchange receipt should have been created")

    def test_outgoing_exchange_still_blocked_when_marked_to_refund(self):
        self._confirm_and_receive_po(2)
        delivery = self.env["stock.picking"].create(
            {
                "picking_type_id": self.picking_type_out.id,
                "partner_id": self.customer.id,
                "location_id": self.stock_location.id,
                "location_dest_id": self.customer_location.id,
                "move_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product.id,
                            "product_uom_qty": 1,
                            "location_id": self.stock_location.id,
                            "location_dest_id": self.customer_location.id,
                        },
                    )
                ],
            }
        )
        delivery.action_confirm()
        self._validate(delivery)
        wizard = self._return_wizard(delivery, 1)
        self.assertTrue(all(wizard.product_return_moves.mapped("to_refund")))

        with self.assertRaises(UserError):
            wizard.action_create_exchanges()

    def test_uninstall_hook_restores_adhoc_view(self):
        adhoc_view = self.env.ref("sale_stock_ux.view_stock_return_picking_form")
        self.assertFalse(adhoc_view.active)

        uninstall_hook(self.env)

        self.assertTrue(adhoc_view.active)

    # Returned quantity after an exchange (purchase_stock_ux)

    def test_exchanged_return_not_counted_as_returned(self):
        order = self._confirm_and_receive_po(2)
        line = order.order_line
        self.assertEqual(line.qty_to_invoice, 2)

        return_picking, exchange_picking = self._exchange(order, 1)
        self._validate(return_picking)

        self.assertEqual(line.qty_returned, 0)
        self.assertEqual(line.qty_received, 1)
        self.assertEqual(line.qty_to_invoice, 2, "An exchange must not reduce what is still to bill")
        self.assertEqual(line.receipt_status, "partial", "The replacement is still pending")

        self._validate(exchange_picking)

        self.assertEqual(line.qty_returned, 0)
        self.assertEqual(line.qty_received, 2)
        self.assertEqual(line.qty_to_invoice, 2)
        self.assertEqual(line.receipt_status, "full")

    def test_return_counts_again_when_exchange_cancelled(self):
        order = self._confirm_and_receive_po(2)
        line = order.order_line

        return_picking, exchange_picking = self._exchange(order, 1)
        self._validate(return_picking)
        exchange_picking.action_cancel()

        self.assertEqual(line.qty_returned, 1)
        self.assertEqual(line.qty_to_invoice, 1)

    def test_plain_refund_return_still_counted(self):
        order = self._confirm_and_receive_po(2)
        line = order.order_line

        action = self._return_wizard(order.picking_ids, 1).action_create_returns()
        self._validate(self.env["stock.picking"].browse(action["res_id"]))

        self.assertEqual(line.qty_returned, 1)
        self.assertEqual(line.qty_to_invoice, 1)
