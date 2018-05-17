from odoo import api, fields, models
import logging, json

class Course(models.Model):
    _name = 'sport.course'
    _description = 'Sport course'

    name = fields.Char(string='Name')
    length = fields.Char(String="cours length (HH:MM)")
    len_hours = fields.Char(default="00", string="Hours")
    len_mins = fields.Char(string="Min", default='00')
    max_attendee = fields.Integer(String="Maximum attendee number")
    course_type_id = fields.Many2one('sport.type_course', string="Course Type")
    color = fields.Char(string="red, green, blue, yellow ...")
    session_ids = fields.One2many('sport.session', 'course_id')

    @api.onchange('len_hours', 'len_mins')
    def update_length(self):
        for record in self:
            self.length = str(self.len_hours) + ":" + str(self.len_mins)

    # Returns all courses
    @api.model
    def search_courses(self):
        course_ids = []
        for course_id in self.search([]):
            session_ids = []

            for session_id in course_id.session_ids:
                subscription_ids = []

                for subscription_id in session_id.subscription_ids:
                    subscription_ids.append({"id": subscription_id.id,
                                             "client_id": subscription_id.client_id.id,
                                             "sub_date": subscription_id.sub_date,
                                             "state": subscription_id.state
                                             })
                session_ids.append({"id": session_id.id,
                                    "title": session_id.name,
                                    "course_id": session_id.course_id.id,
                                    "course_name": session_id.course_id.name,
                                    "start": session_id.start_date,
                                    "end": session_id.end_date,
                                    "color": session_id.color,
                                    "coach": session_id.coach_id.name,
                                    "subscription_ids": subscription_ids
                                    })

            course_ids.append({
                "id": course_id.id,
                "name": course_id.name,
                "length": course_id.length,
                "max_attendee": course_id.max_attendee,
                "course_type_id": course_id.course_type_id.id,
                "course_type_name": course_id.course_type_id.name,
                "course_type_price": course_id.course_type_id.price,
                "session_ids": session_ids
            })

        return json.dumps(course_ids)
        # return course_ids
