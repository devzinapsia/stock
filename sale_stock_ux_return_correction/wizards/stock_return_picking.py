##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models
from odoo.addons.stock.wizard.stock_picking_return import (
    StockReturnPicking as CoreStockReturnPicking,
)


class StockReturnPicking(models.TransientModel):
    _inherit = "stock.return.picking"

    def action_create_exchanges(self):
        # sale_stock_ux blocks this native action whenever a return line is
        # marked "to_refund", and tags the resulting move as
        # `is_exchange_move` so sale_order_line can exclude it from
        # qty_delivered. That tagging only matters for sale (outgoing)
        # exchanges; purchase (incoming) returns have no consumer of it
        # (confirmed: no ingadhoc purchase/stock module reads
        # `is_exchange_move`). So for incoming pickings we call the core
        # Odoo implementation directly, skipping sale_stock_ux's override
        # entirely and restoring native behavior. Sale exchanges keep
        # going through sale_stock_ux unchanged.
        if self.picking_id.picking_type_id.code == "incoming":
            return CoreStockReturnPicking.action_create_exchanges(self)
        return super().action_create_exchanges()
