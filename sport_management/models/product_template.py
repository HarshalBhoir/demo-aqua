from odoo import api, fields, models
import logging


_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_card = fields.Boolean(default=False, string="Est une carte")
    qty_course = fields.Integer()
    course_type_id = fields.Many2one('sport.type_course', string="Type de cours")
    credit_ids = fields.One2many('sport.credit', 'product_id')
