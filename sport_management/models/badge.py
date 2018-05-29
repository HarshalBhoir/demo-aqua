from odoo import api, fields, models
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)

class SportBadge(models.Model):
    _name = 'sport.badge'
    _description = 'Sport Badge'

    name = fields.Char(string='Name')
    barcode = fields.Char(string='Barcode', copy=False, oldname='ean13')
    validity = fields.Datetime(default=datetime.now() + timedelta(days=365))
    account_id = fields.Many2one('sport.account')
    client_id = fields.Many2one('res.partner')
    subscription_ids = fields.One2many('sport.subscription', 'badge_id')
    
    #return integer as message :
    #0 : sub valided
    #1 : sub already valided
    #2 : No credit on card
    #3 : No session soon
    def scan_card(self):
        message = ""
        for badge in self:
            client = badge.client_id
            account = badge.account_id
            now = datetime.now()
            # hour = now + timedelta(hours=1)
            hour = now + timedelta(hours=24)
            lst_subscriptions = client.sub_ids
            type_id = None

            for sub in lst_subscriptions:
                date = datetime.strptime(sub.session_id.start_date, '%Y-%m-%d %H:%M:%S')

                _logger.info(date <= hour)
                if date >= now and date <= hour:
                    type_id = sub.session_id.activity_id.course_type_id
                    credit_id = self.env['sport.credit'].search([('account_id', '=', account.id),('type_id', '=', type_id.id),('number_actual','>', 0)], order='date_buy asc',limit=1)
                    if sub.state == "valid":
                        message = 1
                    else :
                        if not credit_id:
                            message = 2
                        else:
                            credit_id.number_actual = credit_id.number_actual - 1
                            message = 0
                            sub.state = "valid"
                            sub.scan_date = datetime.now()
                            sub.badge_id = badge
                            sub.unit_price = credit_id.product_id.lst_price / credit_id.product_id.qty_course
                            _logger.info(sub.unit_price)
                else:
                    message = 3
            _logger.info(message)
            return message
