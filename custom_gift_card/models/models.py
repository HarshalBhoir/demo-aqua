from odoo import api, fields, models, _
from datetime import timedelta,date,datetime

class ResPartnerBonCadeau(models.Model):
	_inherit = 'res.partner'
	
	list_BC = fields.One2many('bon.cadeau','user_id',ondelete='cascade')
	
class BonCadeau(models.Model):
	_name="bon.cadeau"
	
	ref_com = fields.Many2one('sale.order',String='Référence commande')
	user_id = fields.Many2one('res.partner',ondelete='cascade',invisible=True)
	nom=fields.Char(string='Nom du bon cadeau')
	prix=fields.Float(String='Valeur du bon cadeau')
	date_utilisation=fields.Date(string='Date d\'utilisation')
	date_expiration=fields.Date(string='Date d\'expriation', compute='_compute_date_expiration',store=True)
	statut=fields.Selection([('dispo', 'Disponible'),('utilise', 'Utilisé'),('expire', 'Expiré')],default='dispo')
	warning_delta = fields.Float(string='Jours avant l\'alerte', compute='_compute_warning_delta')
	expiration_delta = fields.Float(string='Jours avant expiration', compute='_compute_expiration_delta')
	
	@api.depends('ref_com')
	def _compute_date_expiration(self):
		for record in self:
			if record.ref_com :
				str_creation = self.env['sale.order'].search([('id','=',self.ref_com.id)]).confirmation_date
				if str_creation:
					date_creation = datetime.strptime(str_creation, '%Y-%m-%d %H:%M:%S')
					record.date_expiration = date_creation.date()+timedelta(days=365)
	
	@api.depends('ref_com')
	def _compute_warning_delta(self):
		for record in self:
			if record.date_expiration:
				today = date.today()
				expiration = datetime.strptime(record.date_expiration,'%Y-%m-%d').date()
				record.warning_delta = (expiration - today -timedelta(days=31)).total_seconds()/86400
	
	@api.depends('ref_com')
	def _compute_expiration_delta(self):
		for record in self:
			if record.date_expiration:
				today = date.today()
				expiration = datetime.strptime(record.date_expiration,'%Y-%m-%d').date()
				record.expiration_delta = (expiration - today).total_seconds()/86400
				
	@api.onchange('date_utilisation')
	def change_statut(self):
		for record in self:
			if record.date_utilisation:
				record.statut='utilise'
			else:
				record.statut='dispo'
			
	@api.multi
	def check_validity(self):
		print("appel")
		result = self.env['bon.cadeau'].search([('statut','=','dispo')])
		for bon_cadeau in result:
			print("boucle")
			if bon_cadeau.expiration_delta<0:
				print("expired")
				bon_cadeau.statut = 'expire'
			if True:
				print("mail")
				template = self.env.ref('custom_gift_card.bon_cadeau_expiration')
				self.env['mail.template'].browse(template.id).send_mail(bon_cadeau.id)
	