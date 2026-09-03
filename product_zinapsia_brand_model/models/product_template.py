from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    zinapsia_brand_id = fields.Many2one(
        comodel_name="zinapsia.product.brand",
        string="Brand",
    )
    zinapsia_model = fields.Char(string="Model")
