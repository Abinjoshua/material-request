# -*- coding: utf-8 -*-
from odoo import models, fields

class MaterialRequestProduct(models.Model):
    _name = "material.request.product"
    _rec_name = "product_id"

    product_id = fields.Many2one('product.product',string='Material')
    purchase_type = fields.Selection([('internal_transfer','Internal Transfer'),('purchase_order','Purchase Order')],string='Purchase Type',required=True)
    quantity = fields.Integer(string='Quantity',required=True)
    material_id = fields.Many2one('material.request',string='Material')
    destination_location_id = fields.Many2one('stock.location',string='Destination Location')


