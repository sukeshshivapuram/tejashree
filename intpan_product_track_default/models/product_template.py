from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # In Odoo 19 new products are created as "Goods" (type='consu') but with
    # "Track Inventory" (is_storable) DISABLED, and it is easy to forget to
    # enable it. Overriding default and create logic AT MODEL LEVEL makes it apply
    # no matter where the product is created (Sales, Purchase, Inventory, import...),
    # while preserving is_storable=False for service products.
    def _default_is_storable(self):
        product_type = self.env.context.get('default_type', 'consu')
        return product_type == 'consu'

    is_storable = fields.Boolean(default=_default_is_storable)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'is_storable' not in vals:
                product_type = vals.get('type') or self.env.context.get('default_type', 'consu')
                vals['is_storable'] = (product_type == 'consu')
        return super().create(vals_list)
