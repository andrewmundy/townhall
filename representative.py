Townhall = namedtuple("Townhall", "description, time, representative")

class Representative(object):
	"""docstring for Representative"""
	def __init__(self, firstname, lastname, city):
		self.firstname = firstname
		self.lastname = lastname
		self.city = city
		self.townhall = None

	def schedule(self, description, time):
		return Townhall(description, time, self)