from odoo import api, fields, models


class KelompokObat(models.Model):
    _name = 'yuksehat.kelompokobat'
    _description = 'Kelompok Obat'

    name = fields.Selection([
        ('tablet', 'Tablet'), 
        ('sirup', 'Sirup'), 
        ('kapsul', 'Kapsul')
    ], string='Nama Kelompok Obat')
    
    kode_kelompok = fields.Char(onchange='_compute_kode_kelompok', string='Kode Kelompok Obat')
    
    @api.onchange('name')
    def _compute_kode_kelompok(self):
        if (self.name == 'tablet'):
            self.kode_kelompok = 'T01'
        elif (self.name == 'sirup'):
            self.kode_kelompok = 'S01'
        elif (self.name == 'kapsul'):
            self.kode_kelompok = 'K01'

    kode_etalase = fields.Char(string='Kode Etalase')
    obat_ids = fields.One2many(comodel_name='yuksehat.obat', 
                                 inverse_name='kelompokobat_id', 
                                 string='Daftar Obat')
    jml_item = fields.Char(compute='_compute_jml_item', string='Jumlah Item')
    
    @api.depends('obat_ids')
    def _compute_jml_item(self):
        for rec in self:
            a = self.env['yuksehat.obat'].search([('kelompokobat_id','=', rec.id)]).mapped('name')
            b = len(a)
            rec.jml_item = b
            rec.daftar = a

    daftar = fields.Char(string='Daftar Isi')
    
    
