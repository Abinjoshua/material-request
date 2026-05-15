# -*- coding: utf-8 -*-
from odoo import models, fields, Command


class Material(models.Model):
    _name = "material.request"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name")
    product_ids = fields.One2many('material.request.product', 'material_id', string='Material Products')
    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirm'), ('done', 'Done'), ('cancel', 'Cancel'),
         ('user_requested', 'User Requested'), ('manager_approved', 'Manager Approved'),
         ('head_approved', 'Head Approved'), ('head_rejected', 'Head Rejected')], string="State",
        default='draft')
    po_count = fields.Integer(string="Purchase Order Count", default=0,
                              compute="compute_po_count")
    internal_transfer_count = fields.Integer(string="Internal Transfer Count", default=0,
                                             compute="compute_internal_transfer_count")
    operation_type_id = fields.Many2one('stock.picking.type', string="Operation Type",required=True)

    def action_request_material(self):
        """ Create a button in Material Request “Request”, when click on that button, change the state into User Requested """
        self.write({'state': 'user_requested'})

    def action_manager_approve(self):
        """ Create a button in Material Request “Manager Approve”, when click on that button, change the state into Manager Approved """
        self.write({'state': 'manager_approved'})

    def action_head_approve(self):
        """ Create a button in Material Request “Head Approve”, when click on that button, change the state into Done,
            it creates purchase order and internal transfer according to the purchase type field in the order lines"""
        int_transfer = self.product_ids.filtered(lambda p: p.purchase_type == 'internal_transfer')
        po = self.product_ids.filtered(lambda p: p.purchase_type == 'purchase_order')

        if int_transfer:
            self.env['stock.picking'].create({
                'partner_id': self.env.user.partner_id.id,
                'picking_type_id': self.operation_type_id.id,
                'material_request': self.name,
                'move_ids': [
                    Command.create({
                        'product_id': record.product_id.id,
                        'product_uom_qty': record.quantity,
                        'location_final_id':record.destination_location_id.id,
                    })for record in int_transfer],
            })
        if po:
            self.env['purchase.order'].create({
                'partner_id': self.env.user.partner_id.id,
                'material_request': self.name,
                'order_line': [
                    Command.create({
                        'product_id': record.product_id.id,
                        'product_qty': record.quantity,
                        'price_unit': record.product_id.standard_price
                    })for record in po]
                })
        self.write({'state':'done'})

    def action_head_reject(self):
        """ Create a button in Material Request “Head Reject”, when click on that button, change the state into Head Rejected """
        int_transfer = self.product_ids.filtered(lambda p: p.purchase_type == 'internal_transfer')
        newlist = [record for record in int_transfer]
        print(newlist)

    def compute_po_count(self):
        """ Function to get the number of purchase orders related to this material """
        for record in self:
            record.po_count = self.env['purchase.order'].search_count(
                [('material_request', '=', self.name)])

    def action_get_purchase_order(self):
        """ Function to create the smart button for the purchase order"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Purchase Order',
            'view_mode': 'list,form',
            'res_model': 'purchase.order',
            'domain': [('material_request', '=', self.name)],
            'context': "{'create': False}"
        }

    def compute_internal_transfer_count(self):
        """ Function to get the number of internal transfers related to this material """
        for record in self:
            record.internal_transfer_count = self.env['stock.picking'].search_count(
                [('material_request', '=', self.name)])

    def action_get_internal_transfer(self):
        """ Function to create the smart button for the internal transfer """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Internal Transfer',
            'view_mode': 'list,form',
            'res_model': 'stock.picking',
            'domain': [('material_request', '=', self.name)],
            'context': "{'create': False}"
        }
    # if int_transfer:
    #     internal = self.env['stock.picking'].create({
    #         'partner_id': self.env.user.partner_id.id,
    #         'picking_type_id': self.operation_type_id.id,
    #         'material_request': self.name,
    #     })
    #     for record in int_transfer:
    #         internal.write({
    #             'move_ids': [
    #                 Command.create({
    #                     'product_id': record.product_id.id,
    #                     'product_uom_qty': record.quantity,
    #                     'location_final_id':record.destination_location_id.id,
    #                 })
    #             ]
    #         })
    #     else:
    #         purchase = self.env['purchase.order'].create({
    #             'partner_id': self.env.user.partner_id.id,
    #             'material_request': self.name,
    #         })
    #         for record in po:
    #             purchase.write({
    #                 'order_line': [
    #                     Command.create({
    #                         'product_id': record.product_id.id,
    #                         'product_qty': record.quantity,
    #                         'price_unit': record.product_id.standard_price
    #                     })
    #                 ]
    #             })
    # self.write({'state':'done'})


