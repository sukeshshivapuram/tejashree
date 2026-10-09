from odoo import models, fields, api, _

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('barcode'):
                vals['barcode'] = self.env['product.product']._get_next_barcode()
        return super().create(vals_list)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def _get_next_barcode(self):
        """ Get the next available barcode from sequence, skipping any that are already assigned. """
        while True:
            barcode = self.env['ir.sequence'].next_by_code('product.barcode')
            if not barcode:
                return False

            # Check if this barcode already exists in standard field
            # Using sudo because we need to check all products/templates regardless of permissions
            # and prevent duplicates across the entire system.
            exists = self.env['product.product'].sudo().search_count([('barcode', '=', barcode)], limit=1) or \
                     self.env['product.template'].sudo().search_count([('barcode', '=', barcode)], limit=1)

            if not exists:
                return barcode

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('barcode'):
                # In Odoo 19, if a template is created, variants are often created automatically.
                # If the template has a barcode, Odoo copies it to the first variant.
                # If no barcode exists anywhere, we generate a new one.
                generate = True
                if vals.get('product_tmpl_id'):
                    tmpl = self.env['product.template'].browse(vals['product_tmpl_id']).sudo()
                    # If template already has a barcode, we might not want to overwrite it 
                    # if this is the first/only variant inheriting the template barcode.
                    if tmpl.exists() and tmpl.barcode:
                        # Check if any other variant of this template already has THIS barcode
                        # If not, this variant can safely use/inherit the template's barcode.
                        other_variant = self.sudo().search_count([
                            ('product_tmpl_id', '=', tmpl.id),
                            ('barcode', '=', tmpl.barcode)
                        ])
                        if not other_variant:
                            generate = False

                if generate:
                    vals['barcode'] = self._get_next_barcode()
        return super().create(vals_list)