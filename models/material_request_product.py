# -*- coding: utf-8 -*-
from odoo import models, fields

class MaterialRequestProduct(models.Model):
    _name = "material.request.product"
    _rec_name = "product_id"

    product_id = fields.Many2one('product.product',string='Material')
    purchase_type = fields.Selection([('internal_transfer','Internal Transfer'),('purchase_order','Purchase Order')],string='Purchase Type')
    quantity = fields.Integer(string='Quantity')
    material_id = fields.Many2one('material',string='Material')


