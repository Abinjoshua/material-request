# -*- coding: utf-8 -*-
from odoo import models, fields, Command

class Material(models.Model):
    _name = "material"

    name = fields.Char(string="Name")
    product_id = fields.Many2many('product.product',string='Material')
    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirm'), ('done', 'Done'), ('cancel', 'Cancel')], string="State",
        default='draft')


    def action_request_material(self):
        # self.write({'state': 'confirm'})
        requested_products = self.product_id
        for product in requested_products:
            if product.qty_available > 0:
                print(product,'In Quantity')
                self.env['stock.picking'].create({
                    'partner_id': self.env.user.partner_id.id,
                    'picking_type_id': 2,
                    'location_id': 5,
                    'location_dest_id': 17,
                    'move_ids': [
                        Command.create({
                            'product_id': product.id,
                            'product_uom_qty': 1,
                        })
                    ]
                })


            else:
                print(product,'Not Available')
                self.env['purchase.order'].create({
                    'partner_id':self.env.user.partner_id.id,
                    'order_line': [
                        Command.create({
                            'product_id': product.id,
                            'product_qty': 1,
                            'price_unit':product.standard_price
                        })
                    ]
                })


