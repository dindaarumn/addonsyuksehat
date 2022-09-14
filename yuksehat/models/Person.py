from odoo import api, fields, models


class Person(models.Model):
    _name = 'yuksehat.person'
    _description = 'New Description'

    name = fields.Char(string='Nama')
    alamat = fields.Char(string='Alamat')
    tgl_lahir = fields.Datetime(string='Tanggal Lahir')

class Kasir(models.Model):
    _name = 'yuksehat.kasir'
    _inherit = 'yuksehat.person'
    _description = 'New Description'

    id_kasir = fields.Char(string='ID Kasir')

class Apoteker(models.Model):
    _name = 'yuksehat.apoteker'
    _inherit = 'yuksehat.person'
    _description = 'New Description'
    
    id_apt = fields.Char(string='ID Apoteker')


    
    
