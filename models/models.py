# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Factura(models.Model):
    _inherit = 'account.invoice'

    imprime_resumen = fields.Boolean(string="Imprime Texto",  required=False)
    texto_impresión = fields.Text(string="Texto para impresión",  required=False, )

class FacturaLineas(models.Model):
    _inherit = 'account.invoice.line'

    @api.onchange('quantity','price_unit','discount')
    def _onchange_sub_total(self):
        self.price_subtotal=round(self.quantity*self.price_unit*((1-self.discount)/100))

class Reparacion(models.Model):
    _inherit = 'mrp.repair'

    equipo_id = fields.Many2one(comodel_name="emsin.equipos", string="Equipo", required=True, )

class Equipo(models.Model):
    _name = 'emsin.equipos'
    _rec_name = "name"
    _description = 'Equipos de clientes'

    name = fields.Char(string="Nombre", required=True, )
    marca = fields.Char(string="Marca",required=False)
    modelo = fields.Char(string="Modelo", required=False)
    patente = fields.Char(string="Patente", required=False)
    nro_serie = fields.Char(string="Serie/Nro. Interno", required=False)
    hrs_km = fields.Char(string="Horas/Kilometros", required=False)
    partner_id = fields.Many2one(comodel_name="res.partner", string="Cliente", required=True, )


class SaleOrderLines(models.Model):
    _inherit = 'sale.order.line'

    sub_total_sr = fields.Integer(string="SubTotal", required=False,compute="_compute_amount_subtotal" )

    @api.one
    @api.depends('product_uom_qty','price_unit','discount')
    def _compute_amount_subtotal(self):
        self.sub_total_sr=self.product_uom_qty*self.price_unit*(1-(self.discount/100))

    @api.multi
    @api.onchange('sub_total_sr')
    def _onchange_sub_total_sr(self):
        amount_untaxed = amount_tax = 0.0
        for i in self:
            amount_untaxed+=i.sub_total_sr
        self.order_id.amount_untaxed=amount_untaxed


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    amount_untaxed = fields.Integer(string="Base Imponible", required=False, compute="_compute_amount_base_imponible")
    amount_total = fields.Integer(string="Base Imponible", required=False, compute="_compute_amount_total")

    @api.one
    @api.depends('order_line')
    def _compute_amount_base_imponible(self):
        suma=0
        for i in self.order_line:
            suma=suma+i.sub_total_sr
        self.amount_untaxed=suma

    @api.onchange('order_line')
    def _onchange_order_line(self):
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line:
                amount_untaxed += line.sub_total_sr
                amount_tax += line.price_tax
            order.update({
                'amount_untaxed': amount_untaxed,
                'amount_tax': amount_tax,
                'amount_total': amount_untaxed + amount_tax,
            })
            self.amount_untaxed=amount_untaxed


    @api.one
    @api.depends('amount_untaxed','amount_tax')
    def _compute_amount_total(self):
        self.amount_total=self.amount_untaxed+self.amount_tax

class NewModule(models.Model):
    _inherit = 'hr.contract'

    media_jornada = fields.Boolean(string="Media Jornada?",  )
