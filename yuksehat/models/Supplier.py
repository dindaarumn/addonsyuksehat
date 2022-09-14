from odoo import api, fields, models


class Supplier(models.Model):
    _name = 'yuksehat.supplier'
    _description = 'New Description'

    name = fields.Char(string='Nama Perusahaan')
    alamat = fields.Char(string='Alamat')
    no_tlp = fields.Char(string='No. Telepon')
    obat_id = fields.Many2many(comodel_name='yuksehat.obat', string='Obat')
    
