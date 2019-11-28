from odoo import api, fields, models, _
import odoo.addons.decimal_precision as dp
import time
import logging



_logger = logging.getLogger(__name__)
DOC_STATES =[('draft','Draft'),
		('open','Need Approval'), 
		('unread','Unread'),
        ('read','Read')]

class doc(models.Model):
	_name 		= "eo.doc"
	_inherit 	= ['mail.thread']
	_description = "Surat"

	
	name = fields.Char(
		string='Nomor',
		readonly=True 
	)
	
	
	subject = fields.Char(
		string='Perihal',
		required=True, 
		readonly=True, 
		states={'draft': [('readonly', False)]}	
	)
	
	
	body = fields.Text(
		string='Isi Surat',
		required=True, 
		readonly=True, 
		states={'draft': [('readonly', False)]},
		compute='_otomatis' 	
	)

	@api.depends('body','doc_template_id')
	def _otomatis(self):
		for record in self:
			self.body = record.doc_template_id.body

	#########################################################################
	# doc template changes
	#########################################################################
	@api.onchange('body','doc_template_id')
	def onchange_doc_template_id(self):
		self.body = self.doc_template_id.body
	
	
	user_id = fields.Many2one(
		string='Dari',
		comodel_name='res.users',
		required=True, 
		readonly=True, 
		states={'draft': [('readonly', False)]}	
	)
	
	
	to_user_ids = fields.One2many(
		string='Kepada',
		comodel_name='eo.to_user',
		inverse_name='doc_id', 
		ondelete='cascade',
		required=True, 
		readonly=True, 
		states={'draft': [('readonly', False)]}	
	)

	cc_user_ids = fields.One2many(
		string='Tembusan',
		comodel_name='eo.cc_user',
		inverse_name='doc_id', 
		ondelete='cascade',
		required=True, 
		readonly=True, 
		states={'draft': [('readonly', False)]}	
	)
	
	
	date = fields.Date(
		string='Tanggal',
		default=lambda self: time.strftime("%Y-%m-%d"),
		required=True, 
		readonly=True, 
		states={'draft': [('readonly', False)]}	
	)
	
	
	doc_type_id = fields.Many2one(
		string='Klasifikasi',
		comodel_name='eo.doc_type',
		required=True, 
		readonly=True, 
		states={'draft': [('readonly', False)]}	
	)

	doc_template_id = fields.Many2one(
		string='Template Surat',
		comodel_name='eo.doc_template',
		required=True, 
		readonly=True, 
		states={'draft': [('readonly', False)]}	
	)
	
	
	read_status = fields.Boolean(
		string='Read',
		readonly=True 
	)

	state = fields.Selection(string="State", selection=DOC_STATES,
                                        required=True,
                                        readonly=True,
                                        default=DOC_STATES[0][0])

	
	doc_history_ids = fields.One2many(
		string='History',
		comodel_name='eo.doc_history',
		inverse_name='doc_id',
		ondelete='cascade', 
		readonly=True 
	)
	
	
	parent_id = fields.Many2one(
		string='Sumber Surat',
		comodel_name='eo.doc',
	)
	
	
	#########################################################################
	#########################################################################
	@api.model
	def create(self, vals):
		if not vals.get('name', False) or vals['name'] == 'New':
			vals['name'] = self.env['ir.sequence'].next_by_code('eo.doc') or 'Error Number!!!'
		return super(doc, self).create(vals)
	
	#########################################################################
	# actions
	#########################################################################
	@api.multi
	def action_draft(self):
		self.state = DOC_STATES[0][0]
	
	@api.multi
	def action_open(self):
		self.state = DOC_STATES[1][0]
		
	@api.multi	
	def action_send(self):
		self.state = DOC_STATES[2][0]

	
	@api.multi
	def action_read(self):
		self.state = DOC_STATES[3][0]
		

	@api.multi		
	def action_reply(self):
		'''
		redirect to eo.doc form view with prefilled values 
		from the old doc
		'''

		######################################################################
		# get the old doc
		######################################################################
		data = self.browse(cr, uid, ids, [])[0]
		# data = self.browse(cr, uid, ids, [])[0]

		######################################################################
		# set defautl values for the redirect 
		######################################################################
		context.update({
			'default_parent_id' : data.id,
			'default_user_id'   : uid,
			'default_to_user_ids' : [(0, 0, {'user_id': data.user_id.id })]
		})

		######################################################################
		# history 
		######################################################################
		self.insert_history(cr, uid, ids[0], 'Replied')

		######################################################################
		# return and show the view  
		######################################################################
		return {
			'name': _('Reply Surat'),
			'view_type': 'form',
			"view_mode": 'form',
			'res_model': 'eo.doc',
			'type': 'ir.actions.act_window',
			'context': context,
		}

	@api.multi
	def action_forward(self,cr,uid,ids,context=None):
		'''
		redirect to eo.doc form view with prefilled values 
		from the old doc
		'''

		######################################################################
		# get the old doc
		######################################################################
		data = self.browse(cr, uid, ids, [])[0]
		# data = self.browse(cr, uid, ids, [])[0]

		######################################################################
		# set defautl values for the redirect 
		######################################################################
		context.update({
			'default_parent_id' : data.id,
			'default_user_id'   : uid,
		})

		######################################################################
		# history 
		######################################################################
		self.insert_history(cr, uid, ids[0], 'Forwarded')

		######################################################################
		# return and show the view  
		######################################################################
		return {
			'name': _('Reply Surat'),
			'view_type': 'form',
			"view_mode": 'form',
			'res_model': 'eo.doc',
			'type': 'ir.actions.act_window',
			'context': context,
		}
		return		
		

	

class to_user(models.Model):
	_name 		= "eo.to_user"
	_rec_name   = 'user_id'
	
	user_id = fields.Many2one(
		string='User',
		comodel_name='res.users',
	)

	
	doc_id = fields.Many2one(
		string='surat',
		comodel_name='eo.doc',
	)

	
	read_status = fields.Boolean(
		string='Read',
	)
		
class cc_user(models.Model):
	_name 		= "eo.cc_user"
	_rec_name   = 'user_id'

	user_id = fields.Many2one(
		string='User',
		comodel_name='res.users',
	)

	
	doc_id = fields.Many2one(
		string='surat',
		comodel_name='eo.doc',
	)

	
	read_status = fields.Boolean(
		string='Read',
	)

class doc_type(models.Model):
	_name 		= "eo.doc_type"
	
	code = fields.Char(
		string='Kode',
		required=True
	)

	
	name = fields.Char(
		string='Name', 
		required=True
	)
		
class doc_template(models.Model):
	_name 		= "eo.doc_template"

	code = fields.Char(
		string='Kode',
		required=True
	)

	
	name = fields.Char(
		string='Name', 
		required=True
	)

	
	body = fields.Text(
		string='Isi',
		required=True
	)
	
class doc_history(models.Model):
	_name 		= "eo.doc_history"
	
	name = fields.Char(
		string='History',
	)

	
	user_id = fields.Many2one(
		string='By',
		comodel_name='res.users',
	)
	
	
	doc_id = fields.Many2one(
		string='Surat',
		comodel_name='eo.doc',
	)
	
	

