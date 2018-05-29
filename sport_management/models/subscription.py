from odoo import api, fields, models, _
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class Subscription(models.Model):
    _name = 'sport.subscription'
    _description = 'Sport subscription'

    name = fields.Char(string='Name', compute="_compute_set_name_client")
    client_id = fields.Many2one('res.partner')
    session_id = fields.Many2one('sport.session')
    sub_date = fields.Datetime(default=datetime.today())
    currency_id = fields.Many2one('res.currency', string='Currency')
    unit_price = fields.Monetary(digits=2, currency_field='currency_id', string="Prix de la séance")
    scan_date = fields.Datetime(sting="Date de validation de la séance")
    badge_id = fields.Many2one('sport.badge')
    state = fields.Selection([
        ('sub', 'Sub'),
        ('valid', 'Valid'),
        ('canceled', 'Canceled'),
        ('waiting', 'Waiting'),
        ('absent', 'Absent'),
    ], string="Subscription state")
    # A customer can't be registered twice in same session
    _sql_constraints = [
        ('unique_client_session', 'unique(session_id, client_id)', 'This customer already registered')
    ]

    @api.depends('client_id')
    def _compute_set_name_client(self):
        for subscription in self:
            subscription.name = subscription.client_id.name

    def set_present(self):
        for sub in self:
            sub.state = 'valid'

    @api.depends('state')
    def _on_change_state(self):
        for subscription in self:
            print(subscription.session_id.attendee_count)

    @api.constrains('session_id')
    def check_validity_subscription(self):
        # Subtract current record
        attendee_count = self.session_id.attendee_count
        if attendee_count >= self.session_id.max_attendee:
            self.waiting()
        else:
            self.write({'state': 'sub'})
            self.email_subscription()

    @api.constrains('session_id')
    def check_schedule_subscription(self):
        subscription_ids = self.search([
            ('id', '!=', self.id),
            ('client_id.id', '=', self.client_id.id),
            ('state', '=', 'sub')
        ])

        for subscription_id in subscription_ids:
            if self.session_id.start_date <= subscription_id.session_id.end_date and \
                    self.session_id.end_date >= subscription_id.session_id.start_date:
                raise ValidationError(_('This customer already have session at this moment.'))

    # function to change state of subscription
    @api.one
    def subscribe(self):
        self.check_validity_subscription()
        self.check_schedule_subscription()

    # function to change state of subscription
    @api.one
    def valid(self):
        self.write({'state': 'valid'})
        self.email_validation()

    # function to change state of subscription
    @api.one
    def cancel(self):
        self.write({'state': 'canceled'})
        self.email_cancellation()

    # function to change state of subscription
    @api.one
    def waiting(self):
        self.write({'state': 'waiting'})
        self.email_waiting()

    # function to change state of subscription
    @api.one
    def absent(self):
        self.write({'state': 'absent'})
        self.email_absent()

    # function to prepare an absent email, it call send_mail() function to create and send it
    @api.multi
    def email_subscription(self):
        subject = 'The subscription for ' + self.client_id.name + ' has been registered'
        email_to = self.env.user.company_id.email
        body = '<p>This customer :<br />'
        body += self.client_id.name + '<br />'
        if self.client_id.email:
            body += 'Email : ' + self.client_id.email + '<br />'
        if self.client_id.phone:
            body += 'Phone : ' + self.client_id.phone + '<br />'
        if self.client_id.mobile:
            body += 'Mobile : ' + self.client_id.mobile + '<br /><br />'
        body += 'Has been registered to the session : <br />'
        body += self.session_id.name + '<br />'
        body += 'At : ' + self.session_id.start_date + '<br />'
        body += 'Hours : ' + str(self.session_id.activity_id.length) + '<br /><br />'

        self.send_mail(subject, email_to, body)

    # function to prepare an absent email, it call send_mail() function to create and send it
    @api.multi
    def email_validation(self):
        subject = self.client_id.name + ' was present at the session.'
        email_to = self.env.user.company_id.email
        body = '<p>This customer :<br />'
        body += self.client_id.name + '<br />'
        if self.client_id.email:
            body += 'Email : ' + self.client_id.email + '<br />'
        if self.client_id.phone:
            body += 'Phone : ' + self.client_id.phone + '<br />'
        if self.client_id.mobile:
            body += 'Mobile : ' + self.client_id.mobile + '<br /><br />'
        body += 'Has been participated to the session : <br />'
        body += self.session_id.name + '<br />'
        body += 'At : ' + self.session_id.start_date + '<br />'
        body += 'Hours : ' + str(self.session_id.activity_id.length) + '<br /><br />'

        self.send_mail(subject, email_to, body)

    # function to prepare an absent email, it call send_mail() function to create and send it
    @api.multi
    def email_waiting(self):
        subject = self.client_id.name + ' has been registered in waiting list'
        email_to = self.env.user.company_id.email
        body = '<p>This customer :<br />'
        body += self.client_id.name + '<br />'
        if self.client_id.email:
            body += 'Email : ' + self.client_id.email + '<br />'
        if self.client_id.phone:
            body += 'Phone : ' + self.client_id.phone + '<br />'
        if self.client_id.mobile:
            body += 'Mobile : ' + self.client_id.mobile + '<br /><br />'
        body += 'Has been registered in waiting list to the session : <br />'
        body += self.session_id.name + '<br />'
        body += 'At : ' + self.session_id.start_date + '<br />'
        body += 'Hours : ' + str(self.session_id.activity_id.length) + '<br /><br />'

        self.send_mail(subject, email_to, body)

    # function to prepare an absent email, it call send_mail() function to create and send it
    @api.multi
    def email_cancellation(self):
        waiting_list = '<table border="1"><thead><tr><th>Date</th><th>Customer</th><th>Phone</th><th>mobile</th></thead><tbody>'

        # Get and order waiting subscriptions
        subscriptions_waitings = self.search([('state', '=', 'waiting')], order="sub_date")

        # Build waiting list
        for subscription in subscriptions_waitings:
            waiting_list += '<tr>'

            waiting_list += '<td>' + subscription.sub_date + '</td>'
            waiting_list += '<td>' + subscription.client_id.name + '</td>'

            if subscription.client_id.phone:
                waiting_list += '<td>' + subscription.client_id.phone + '</td>'
            else:
                waiting_list += '<td></td>'

            if subscription.client_id.mobile:
                waiting_list += '<td>' + subscription.client_id.mobile + '</td>'
            else:
                waiting_list += '<td></td>'

            waiting_list += '</tr>'

        waiting_list += '</tbody></table>'

        subject = self.client_id.name + ' has been canceled its registration'
        email_to = self.env.user.company_id.email
        body = '<p>This customer :<br />'
        body += self.client_id.name + '<br />'
        if self.client_id.email:
            body += 'Email : ' + self.client_id.email + '<br />'
        if self.client_id.phone:
            body += 'Phone : ' + self.client_id.phone + '<br />'
        if self.client_id.mobile:
            body += 'Mobile : ' + self.client_id.mobile + '<br /><br />'
        body += 'Has been canceled its registration to the session : <br />'
        body += self.session_id.name + '<br />'
        body += 'At : ' + self.session_id.start_date + '<br />'
        body += 'Hours : ' + str(self.session_id.activity_id.length) + '<br /><br />'
        body += waiting_list + '</p>'

        self.send_mail(subject, email_to, body)

    # function to prepare an absent email, it call send_mail() function to create and send it
    @api.multi
    def email_absent(self):
        subject = self.client_id.name + ' has been absent.'
        email_to = self.env.user.company_id.email
        body = '<p>' + self.client_id.name + ', was absent at the ' + self.session_id.name + \
               ' session at ' + self.session_id.start_date + ' for ' \
               + str(self.session_id.activity_id.length) + '.</p>'

        self.send_mail(subject, email_to, body)

    # function called by over function to send create and email
    @api.multi
    def send_mail(self, subject, email_to, body):
        mail_pool = self.env['mail.mail']

        values = {}
        values.update({'subject': subject})
        values.update({'email_to': email_to})
        values.update({'body_html': body})

        msg_id = mail_pool.create(values)

        if msg_id:
            mail_pool.send([msg_id])

    # function to prepare an reminder email, it call send_mail() function to create and send it
    @api.multi
    def email_reminder(self):

        # Initiate an array who will get all subscriber needing to be remind
        subscriptions_need_remind = self.get_subscription_need_remind()

        str_subs = '<table border="1"><thead><tr><th>Customer</th><th>Session</th><th>Phone</th><th>mobile</th></thead><tbody>'

        # Create list string of subscriptions need to be remind
        for subscription_id in subscriptions_need_remind:
            str_subs += '<tr>'
            str_subs += '<td>' + subscription_id.client_id.name + '</td>'
            str_subs += '<td>' + subscription_id.session_id.name + '</td>'

            if subscription_id.client_id.phone:
                str_subs += '<td>' + subscription_id.client_id.phone + '</td>'
            else:
                str_subs += '<td></td>'

            if subscription_id.client_id.mobile:
                str_subs += '<td>' + subscription_id.client_id.mobile + '</td>'
            else:
                str_subs += '<td></td>'

            str_subs += '<tr>'
        str_subs += '</tbody></table>'

        subject = 'These customers have subscribed to a session tomorrow.'
        email_to = self.env.user.company_id.email
        body = '<p>These customers have subscribed to a session tomorrow.<br />'
        body = body + str_subs

        # call function to send the email
        self.send_mail(subject, email_to, body)

    # Returns all subscriptions who need to be reminding.
    @api.multi
    def get_subscription_need_remind(self):
        # Initiate an array who will get all subscriber needing to be remind
        subscriptions_need_remind = []

        # All subscription is tested to know if they need to be remind
        for subscription_id in self.search([]):

            # Exit the first empty subscription
            if not subscription_id.session_id.id:
                continue

            # Subtract one day to the start_date session
            date_start = datetime.strptime(subscription_id.session_id.start_date, '%Y-%m-%d %H:%M:%S') - timedelta(
                days=1)
            date_today = datetime.now()

            # Compare year, month and day of date_start and current date
            if date_start.day == date_today.day and date_start.month == date_today.month and date_start.year == date_today.year:
                # The subscriber need to be remind, it add to the list
                subscriptions_need_remind.append(subscription_id)

        return subscriptions_need_remind
