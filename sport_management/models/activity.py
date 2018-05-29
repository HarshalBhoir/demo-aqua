from odoo import api, fields, models
import logging, json

class Activity(models.Model):
    _name = 'sport.activity'
    _description = 'Sport activity'

    name = fields.Char(string='Name')
    length = fields.Char(String="cours length (HH:MM)")
    len_hours = fields.Char(default="00", string="Hours")
    len_mins = fields.Char(string="Min", default='00')
    max_attendee = fields.Integer(String="Maximum attendee number")
    min_attendee = fields.Integer(String="Minimum attendee number")
    course_type_id = fields.Many2one('sport.type_course', string="Type de cours requis")
    color = fields.Char(string="red, green, blue, yellow ...")
    session_ids = fields.One2many('sport.session', 'activity_id')

    @api.onchange('len_hours', 'len_mins')
    def update_length(self):
        for record in self:
            self.length = str(self.len_hours) + ":" + str(self.len_mins)

    # Returns all activities
    @api.model
    def search_activities(self):
        activity_ids = []
        for activity_id in self.search([]):
            session_ids = []

            for session_id in activity_id.session_ids:
                subscription_ids = []

                for subscription_id in session_id.subscription_ids:
                    subscription_ids.append({"id": subscription_id.id,
                                             "client_id": subscription_id.client_id.id,
                                             "sub_date": subscription_id.sub_date,
                                             "state": subscription_id.state
                                             })
                session_ids.append({"id": session_id.id,
                                    "title": session_id.name,
                                    "activity_id": session_id.activity_id.id,
                                    "activity_name": session_id.activity_id.name,
                                    "start": session_id.start_date,
                                    "end": session_id.end_date,
                                    "color": session_id.color,
                                    "coach": session_id.coach_id.name,
                                    "subscription_ids": subscription_ids
                                    })

            activity_ids.append({
                "id": activity_id.id,
                "name": activity_id.name,
                "length": activity_id.length,
                "max_attendee": activity_id.max_attendee,
                "activity_type_id": activity_id.activity_type_id.id,
                "activity_type_name": activity_id.activity_type_id.name,
                "activity_type_price": activity_id.activity_type_id.price,
                "session_ids": session_ids
            })

        return json.dumps(activity_ids)
        # return activity_ids
