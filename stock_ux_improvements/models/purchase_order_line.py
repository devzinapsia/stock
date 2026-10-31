##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import api, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    @api.depends("move_ids.picking_id.return_ids.state")
    def _compute_qty_returned(self):
        # purchase_stock_ux counts every done vendor return marked "to_refund"
        # as returned, and subtracts that from qty_to_invoice on lines billed
        # on ordered quantities. A return made with "Create exchanges" is
        # followed by the replacement receipt (a return of that return), so
        # the vendor never owes a refund for it: counting it left the order
        # waiting for a negative bill forever, and "Create Bill" would issue
        # a credit note nobody asked for. Returns that have a live (not
        # cancelled) return of their own are therefore not counted; if the
        # replacement is cancelled, the return counts again.
        super()._compute_qty_returned()
        for line in self:
            exchanged_moves = line.move_ids.filtered(
                lambda move: move.state == "done"
                and move.to_refund
                and move._is_purchase_return()
                and move.picking_id.return_ids.filtered(lambda picking: picking.state != "cancel")
            )
            line.qty_returned -= sum(
                move.product_uom._compute_quantity(move.product_uom_qty, line.product_uom_id)
                for move in exchanged_moves
            )
