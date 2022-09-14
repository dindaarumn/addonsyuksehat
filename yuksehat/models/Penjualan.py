from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class Penjualan(models.Model):
    _name = 'yuksehat.penjualan'
    _description = 'Penjualan'

    name = fields.Char(string='No. Struk')
    nama_pembeli = fields.Char(string='Nama Pembeli')
    tgl_penjualan = fields.Datetime(
        string='Tanggal Transaksi',
        default=fields.Datetime.now())
    total_bayar = fields.Integer(
        string='Total Pembayaran',
        compute='_compute_totalbayar')
    detailpenjualan_ids = fields.One2many(
        comodel_name='yuksehat.detailpenjualan',
        inverse_name='penjualan_id',
        string='Detail Penjualan')

    @api.depends('detailpenjualan_ids')
    def _compute_totalbayar(self):
        for line in self:
            result = sum(self.env['yuksehat.detailpenjualan'].search(
                [('penjualan_id', '=', line.id)]).mapped('subtotal'))
            line.total_bayar = result


class DetailPenjualan(models.Model):
    _name = 'yuksehat.detailpenjualan'
    _description = 'Detail'

    name = fields.Char(string='Nama')
    penjualan_id = fields.Many2one(
        comodel_name='yuksehat.penjualan',
        string='Detail Penjualan')
    obat_id = fields.Many2one(
        comodel_name='yuksehat.obat',
        string='List Obat')
    harga_satuan = fields.Integer(
        string='Harga Satuan',
        onchange='_onchange_obat_id')
    qty = fields.Integer(string='Quantity')
    subtotal = fields.Integer(compute='_compute_subtotal', string='Subtotal')

    @api.depends('harga_satuan', 'qty')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.qty * line.harga_satuan

    @api.onchange('obat_id')
    def _onchange_obat_id(self):
        if self.obat_id.harga_jual:
            self.harga_satuan = self.obat_id.harga_jual

    @api.model
    def create(self, vals):
        line = super(DetailPenjualan, self).create(vals)
        if line.qty:
            self.env['yuksehat.obat'].search(
                [('id', '=', line.obat_id.id)]
            ).write({'stok': line.obat_id.stok - line.qty})

        return line

    @api.ondelete(at_uninstall=False)
    def __ondelete_penjualan(self):
        if self.detailpenjualan_ids:
            penjualan = []
            for line in self:
                penjualan = self.env['yuksehat.detailpenjualan'].search(
                    [('penjualan_id', '=', line.id)])
                print(penjualan)

            for ob in penjualan:
                print(ob.obat_id.name + ' ' + str(ob.qty))
                ob.obat_id.stok += ob.qty

    def unlink(self):
        if self.detailpenjualan_ids:
            penjualan = []
            for line in self:
                penjualan = self.env['yuksehat.detailpenjualan'].search(
                    [('penjualan_id', '=', line.id)])
                print(penjualan)

            for ob in penjualan:
                print(ob.obat_id.name + ' ' + str(ob.qty))
                ob.obat_id.stok += ob.qty

        line = super(Penjualan, self).unlink()

    @api.constrains('qty')
    def check_quantity(self):
        for line in self:
            if line.qty < 1:
                raise ValidationError('Jumlah pembelian harus minimal 1, silahkan input dengan benar!')
            elif line.obat_id.stok < line.qty:
                raise ValidationError('Stok yang tersedia tidak mencukupi.')

    _sql_constraints = [
        ('no_struk_unik', 'unique (name)', 'Nomor Struk tidak boleh sama!')
    ]

    def write(self, vals):
        for rec in self:
            a = self.env['yuksehat.detailpenjualan'].search([('penjualan_id', '=', rec.id)])
            print(a)
            for data in a:
                print(str(data.obat_id.name) + ' ' + str(data.qty) + ' ' + str(data.obat_id.stok))
                data.obat_id.stok += data.qty
        record = super(Penjualan, self).write(vals)
        for rec in self:
            b = self.env['yuksehat.detailpenjualan'].search([('penjualan_id', '=', rec.id)])
            print(a)
            print(b)
            for databaru in b:
                if databaru in a:
                    print(str(databaru.obat_id.name) + ' ' + str(databaru.qty) + ' ' + str(databaru.obat_id.stok))
                    databaru.obat_id.stok -= databaru.qty
                else:
                    pass
        return record