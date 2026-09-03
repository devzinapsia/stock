from odoo import fields, models


class ZinapsiaProductBrand(models.Model):
    """Configurable catalog of product brands, namespaced under 'zinapsia'
    to avoid colliding with the unrelated 'product.brand' model shipped by
    other, non-Zinapsia modules (OCA and others)."""

    _name = "zinapsia.product.brand"
    _description = "Product Brand"
    _order = "sequence, name"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(required=True, translate=True, tracking=True)
    active = fields.Boolean(default=True)
    sequence = fields.Integer(default=10)

    _name_uniq = models.Constraint(
        "unique(name)",
        "A brand with this name already exists.",
    )
