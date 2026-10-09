from odoo import fields, models


class PrintLabelTypePy(models.Model):
    _name = "print.label.type"
    _description = 'Label Types'
    _order = 'sequence'

    sequence = fields.Integer(default=100)
    name = fields.Char(required=True, translate=True)
    code = fields.Char(required=True, readonly=True)
    active = fields.Boolean(default=True)

    _code_unique = models.Constraint('unique (code)', 'Code of a print label type must be unique.')
