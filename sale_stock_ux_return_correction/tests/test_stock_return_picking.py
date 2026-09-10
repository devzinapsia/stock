from odoo.addons.stock.tests.common import TestStockCommon
from odoo.exceptions import UserError

from .. import uninstall_hook


class TestStockReturnPickingReturnCorrection(TestStockCommon):
    def _do_picking(self, picking_type, location_id, location_dest_id, qty):
        picking = self.PickingObj.create(
            {
                "picking_type_id": picking_type.id,
                "location_id": location_id.id,
                "location_dest_id": location_dest_id.id,
            }
        )
        self.MoveObj.create(
            {
                "product_id": self.productA.id,
                "product_uom_qty": qty,
                "product_uom": self.uom_unit.id,
                "picking_id": picking.id,
                "location_id": location_id.id,
                "location_dest_id": location_dest_id.id,
            }
        )
        picking.action_confirm()
        picking.action_assign()
        picking.move_ids.quantity = qty
        picking.move_ids.picked = True
        picking.button_validate()
        return picking

    def _create_return_wizard(self, picking, qty):
        wizard = (
            self.env["stock.return.picking"]
            .with_context(active_id=picking.id, active_ids=picking.ids, active_model="stock.picking")
            .create({})
        )
        wizard.product_return_moves.quantity = qty
        return wizard

    def test_view_deactivated(self):
        adhoc_view = self.env.ref("sale_stock_ux.view_stock_return_picking_form")
        self.assertFalse(adhoc_view.active)

    def test_incoming_exchange_allowed_even_when_marked_to_refund(self):
        picking = self._do_picking(self.picking_type_in, self.supplier_location, self.stock_location, 2)
        wizard = self._create_return_wizard(picking, 2)
        self.assertTrue(all(wizard.product_return_moves.mapped("to_refund")))

        action = wizard.action_create_exchanges()

        return_picking = self.env["stock.picking"].browse(action["res_id"])
        exchange_picking = self.env["stock.picking"].search([("return_id", "=", return_picking.id)])
        self.assertTrue(exchange_picking, "The native exchange receipt should have been created")

    def test_outgoing_exchange_still_blocked_when_marked_to_refund(self):
        self._do_picking(self.picking_type_in, self.supplier_location, self.stock_location, 2)
        picking = self._do_picking(self.picking_type_out, self.stock_location, self.customer_location, 1)
        wizard = self._create_return_wizard(picking, 1)
        self.assertTrue(all(wizard.product_return_moves.mapped("to_refund")))

        with self.assertRaises(UserError):
            wizard.action_create_exchanges()

    def test_uninstall_hook_restores_adhoc_view(self):
        adhoc_view = self.env.ref("sale_stock_ux.view_stock_return_picking_form")
        self.assertFalse(adhoc_view.active)

        uninstall_hook(self.env)

        self.assertTrue(adhoc_view.active)
