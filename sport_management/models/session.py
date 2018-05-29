from odoo import api, fields, models
import logging, json
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)


class Session(models.Model):
    _name = 'sport.session'
    _description = 'Sport session'

    name = fields.Char(string='Name')
    activity_id = fields.Many2one('sport.activity', string="Activitées")
    start_date = fields.Datetime(string="Start date")
    end_date = fields.Datetime(string="End date")
    coach_id = fields.Many2one('res.partner', string="Coach")
    attendee_count = fields.Integer(String="Attendee number", compute="_compute_attendee_count")
    subscription_ids = fields.One2many('sport.subscription', 'session_id')
    waiting_attendee_count = fields.Integer(String="Waiting attendee count", compute="_compute_waiting_attendee_count")
    canceled_attendee_count = fields.Integer(String="Canceled attendee count",
                                             compute="_compute_canceled_attendee_count")
    state = fields.Selection(string='state', required=False,
                             selection=[('done', 'Done'), ('cancel', 'Canceled'), ('valid', 'Valid')], default="valid")
    day = fields.Char(String="Days", compute="_compute_session_day")
    color = fields.Char(compute="_compute_color")
    max_attendee = fields.Integer(String="Maximum attendee number", compute="_compute_max_attendee")

    @api.depends('subscription_ids')
    def _compute_attendee_count(self):
        for session in self:
            session.attendee_count = 0
            for sub in session.subscription_ids:
                if sub.state == 'sub':
                    session.attendee_count += 1

    @api.depends('subscription_ids')
    def _compute_waiting_attendee_count(self):
        for session in self:
            session.waiting_attendee_count = 0
            for sub in session.subscription_ids:
                if sub.state == 'waiting':
                    session.waiting_attendee_count += 1

    @api.depends('subscription_ids')
    def _compute_canceled_attendee_count(self):
        for session in self:
            session.canceled_attendee_count = 0
            for sub in session.subscription_ids:
                if sub.state == 'canceled':
                    session.canceled_attendee_count += 1

    @api.onchange('start_date')
    def _compute_session_day(self):
        for session in self:
            if session.start_date:
                date = datetime.strptime(session.start_date, '%Y-%m-%d %H:%M:%S')

    def search_all_session(self):
        return self.env['sport.session'].search([('state', 'like', 'valid')])

    @api.depends("activity_id")
    def _compute_color(self):
        for session in self:
            session.color = session.activity_id.color

    # Auto complet end_date in form field
    @api.onchange('start_date')
    def _compute_end_date(self):
        for session in self:
            if session.activity_id.length:
                length = datetime.strptime(session.activity_id.length, '%H:%M').time()
                date = datetime.strptime(session.start_date, '%Y-%m-%d %H:%M:%S')
                session.end_date = date + timedelta(hours=length.hour, minutes=length.minute)

    # Print calendar to PDF
    @api.multi
    def print_calendar(self):
        print('Print pdf')

    # Returns a json contains all needed sessions data's to build web calendar.
    @api.model
    def search_session_and_subscription(self):
        sessions = []
        for session in self.search([]):
            subscriptions = []
            for subscription in session.subscription_ids:
                subscriptions.append({"id": subscription.id,
                                      "client_id": subscription.client_id.id,
                                      "sub_date": subscription.sub_date,
                                      "state": subscription.state
                                      })

            sessions.append({"id": session.id,
                             "title": session.name,
                             "activity_id": session.activity_id.id,
                             "activity_name": session.activity_id.name,
                             "start": session.start_date,
                             "end": session.end_date,
                             "color": session.color,
                             "coach": session.coach_id.name,
                             "subscriptions": subscriptions
                             })

        return json.dumps(sessions)

    def _compute_max_attendee(self):
        for session in self:
            self.max_attendee = session.activity_id.max_attendee
        
    @api.onchange('activity_id')
    def _update_session_end_date(self):
        for session in self:
            _logger.info(session.activity_id.length)
            if session.activity_id.length != False and session.start_date != False:
                length = datetime.strptime(session.activity_id.length, '%H:%M').time()
                date = datetime.strptime(session.start_date, '%Y-%m-%d %H:%M:%S')
                _logger.info(length.second)
                session.end_date = date + timedelta(hours=length.hour, minutes=length.minute)
                _logger.info('aa')
