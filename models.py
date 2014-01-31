from datetime import datetime
from utils import get_attrs, get_uuid
from config import app, db

class STATUS:
	introduced = 1
	queued = 2
	converted = 3
	completed = 4
	failed = 5

class PRIORITY:
	high = 0
	medium = 1
	low = 2

	@classmethod
	def get_values(cls):
		return map(
			lambda attr: getattr(cls, attr), 
			get_attrs(cls)
		)

from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

class Account(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(32), index = True, unique = True)
	password_hash = db.Column(db.Text)
	callback = db.Column(db.Text)

	def hash_password(self, password):
		self.password_hash = pwd_context.encrypt(password)
		
	def verify_password(self, password):
		return pwd_context.verify(password, self.password_hash)

	def generate_auth_token(self, expiration = 600):
		s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
		return s.dumps({ 'id': self.id })

	@staticmethod
	def verify_auth_token(token):
		s = Serializer(app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except SignatureExpired:
			return None # valid token, but expired
		except BadSignature:
			return None # invalid token
		user = Account.query.get(data['id'])
		return user

	def __repr__(self):
		return '<Account %r>' % self.username


class File(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	filename = db.Column(db.Text)
	location = db.Column(db.Text)
	priority = db.Column(db.Integer, index = True)
	timestamp = db.Column(db.DateTime)
	account_ref = db.Column(db.Integer, db.ForeignKey('account.id'))
	account_instance = db.relationship('Account',
	 	backref=db.backref('file', lazy='dynamic'))
	
	def __init__(self, filename, location, account_instance, priority = PRIORITY.medium):
		self.filename = filename
		self.location = location
		self.account_instance = account_instance
		self.priority = priority
		self.timestamp = datetime.utcnow()

	def __repr__(self):
		return '<File %r - %r>' % (self.account_instance, self.location)

class Conversion(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	output_format = db.Column(db.String(10))
	status = db.Column(db.Integer, index = True)
	doc_id = db.Column(db.String(40), index = True)
	signed_url = db.Column(db.Text)

	file_ref = db.Column(db.Integer, db.ForeignKey('file.id'))
	file_instance = db.relationship('File',
        backref=db.backref('conversion', lazy='dynamic'))

	def __init__(self, file_instance, output_format, status = STATUS.introduced):
		self.file_instance = file_instance
		self.output_format = output_format
		self.status = status
		self.doc_id = get_uuid()

	def __repr__(self):
		return '<Conversion %r - %r>' % (self.file_instance, self.output_format)

	@classmethod
	def register_file(cls, filename, location, account_instance, output_formats, priority):
		data = {}
		f = File(filename = filename, location = location, account_instance = account_instance, priority = priority)
		db.session.add(f)
		for output_format in set(output_formats):
			c = cls(file_instance = f, output_format = output_format)
			data[output_format] = c.doc_id
			db.session.add(c)
		db.session.commit()
		return data

	@classmethod
	def get_requests_by_priority(cls, status = STATUS.introduced, limit = 5):
		return cls.query\
				.filter_by(status = status)\
				.join(File)\
				.order_by(File.priority)\
				.limit(limit).all()