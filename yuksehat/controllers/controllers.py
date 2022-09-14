from crypt import methods
import json
from odoo import http, models, fields
from odoo.http import request


class Yuksehat(http.Controller):
    @http.route('/yuksehat/getobat', auth='public', method=['GET'])
    def getObat(self, **kw):
        obat = request.env['yuksehat.obat'].search([])
        items = []

        for item in obat:
            items.append({
                'nama_obat': item.name,
                'harga_jual': item.harga_jual,
                'stok': item.stok
            })
        
        return json.dumps(items)

    @http.route('/yuksehat/getsupplier', auth='public', method=['GET'])
    def getSupplier(self, **kw):
        supplier = request.env['yuksehat.supplier'].search([])
        items = []

        for item in supplier:
            items.append({
                'nama_perusahaan': item.name,
                'alamat': item.alamat,
                'no_telepon': item.no_tlp,
                'obat_id': item.obat_id[0].name
            })
        
        return json.dumps(items)