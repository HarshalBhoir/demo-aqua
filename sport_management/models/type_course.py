from odoo import api, fields, models


class TypeCourse(models.Model):
    _name = 'sport.type_course'
    _description = 'Sport type course'

    name = fields.Char(string='Name')
    activity_ids = fields.One2many('sport.activity','course_type_id')
    session_ids = fields.Many2many('sport.session', 'course', 'session_ids')