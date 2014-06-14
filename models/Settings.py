

class SettingsSingleton():

	_instance = None

	min_prime_size = 10

	max_iteration_count = 5

	def __init__(self):
		self.listeners = []

	@classmethod
	def get_instance(cls):
		if cls._instance == None:
			cls._instance = SettingsSingleton()

		return cls._instance

	def get_prime_size(self):
		return self.min_prime_size

	def get_iteration_count(self):
		return self.max_iteration_count

	def set_prime_size(self, size):
		self.min_prime_size = size

	def set_iteration_count(self, count):
		self.max_iteration_count = count