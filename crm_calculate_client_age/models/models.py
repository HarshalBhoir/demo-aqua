# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta
import logging
_logger = logging.getLogger(__name__)

class crm_calculate_client_age(models.Model):
    _inherit = 'res.partner'

    age = fields.Integer(compute="_calculate_age")
    # age = fields.Integer()

    @api.depends('x_studio_field_0yAlw')
    def _calculate_age(self):
        for record in self:
            if record.x_studio_field_0yAlw:
                born = datetime.strptime(record.x_studio_field_0yAlw, '%Y-%m-%d %H:%M:%S')
                _logger.info('---------------------- VAR : born --------------------------------')
                _logger.info(born)
                date_today = datetime.now()

                record.age = date_today.year - born.year