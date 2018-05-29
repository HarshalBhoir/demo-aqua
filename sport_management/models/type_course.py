from odoo import api, fields, models


class TypeCourse(models.Model):
    _name = 'sport.type_course'
    _description = 'Sport type course'

    name = fields.Char(string='Name')
    price = fields.Float(string='Course price')
    product_id = fields.Many2one(comodel_name='product.template', string='Product for quotation', required=False)
    activity_ids = fields.One2many('sport.activity','course_type_id')
    session_ids = fields.Many2many('sport.session', 'course', 'session_ids')