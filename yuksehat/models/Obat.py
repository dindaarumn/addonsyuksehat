from odoo import api, fields, models


class Obat(models.Model):
    _name = 'yuksehat.obat'
    _description = 'New Description'

    name = fields.Char(string='Nama Obat')
    harga_beli = fields.Integer(string='Harga Modal', required=True)
    harga_jual = fields.Integer(string='Harga Jual', required=True)
    kelompokobat_id = fields.Many2one(comodel_name='yuksehat.kelompokobat', 
                                      string='Kelompok Obat',
                                      ondelete='cascade')
    supplier_id = fields.Many2many(comodel_name='yuksehat.supplier', string='Supplier')
    stok = fields.Integer(string='Stok')
    
    
    
    
