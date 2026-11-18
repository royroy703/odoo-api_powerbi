from odoo import http
from odoo.http import request
import json

class PowerBIController(http.Controller):

    @http.route('/api/powerbi/data', type='http', auth='public', methods=['GET'], website=False, csrf=False, cors='*')
    def get_powerbi_data(self, token=None, **kwargs):
        
        # 1. Validación amigable para Power BI (retorna 200 OK con mensaje de error en lugar de 401)
        if token != 'TOKEN_SECRETO_CERVECERIA_2026':
            return request.make_response(
                json.dumps({'status': 'error', 'message': 'Acceso no autorizado', 'data': []}),
                headers=[('Content-Type', 'application/json')]
            )
            
        # 2. Extracción de datos
        records = request.env['hr.attendance'].sudo().search([])
        
        data = []
        for rec in records:
            data.append({
                'id': rec.id,
                'empleado': rec.employee_id.name if rec.employee_id else 'Desconocido',
                'entrada': str(rec.check_in) if rec.check_in else '',
                'salida': str(rec.check_out) if rec.check_out else '',
                'horas_trabajadas': round(rec.worked_hours, 2)
            })
            
        # 3. Respuesta JSON limpia
        return request.make_response(
            json.dumps({"status": "success", "rows": len(data), "data": data}),
            headers=[('Content-Type', 'application/json')]
        )