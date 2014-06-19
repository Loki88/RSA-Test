import shelve, inspect
from models import SettingsSingleton
from models.PrimalityTest import MillerRabinTest
from models.NumberFactory import NumberFactorySingleton
from models.FactorizationMethod import PMinusOneAndExponentMethod
from models.NumberGenerator import StrongPrimeGenerator, PrimeGenerator

class SettingsControllerSingleton():

	settings_store = "settings"

	_instance = None

	listeners = []

	def __init__(self):
		self.initialize()

	@classmethod
	def get_instance(cls):
		if cls._instance == None:
			cls._instance = SettingsControllerSingleton()

		return cls._instance

	def get_primality_test(self):
		test = NumberFactorySingleton.get_instance().get_primality_test()
		return test

	def get_factorization_method(self):
		return SettingsSingleton.get_instance().get_factorization_method()

	def set_primality_test(self, test):
		if inspect.isclass(test):
			test = test()
		NumberFactorySingleton.get_instance().set_primality_test(test)
		self.notifica()

	def set_factorization_method(self, method):
		if inspect.isclass(method):
			method = method()
		SettingsSingleton.get_instance().set_factorization_method(method)
		self.notifica()

	def set_prime_size(self, size):
		SettingsSingleton.get_instance().set_prime_size(size)
		self.notifica()

	def set_iteration_count(self, count):
		SettingsSingleton.get_instance().set_iteration_count(count)
		self.notifica()

	def get_prime_size(self):
		return SettingsSingleton.get_instance().get_prime_size()

	def get_iteration_count(self):
		return SettingsSingleton.get_instance().get_iteration_count()

	def store(self):
		self.update()

	def initialize(self):
		db = shelve.open(self.settings_store)
		if db.has_key('synchronized'):
			if db['synchronized']:
				if db.has_key('prime_size'):
					self.set_prime_size(db['prime_size'])
				if db.has_key('max_iteration_count'):
					self.set_iteration_count(db['max_iteration_count'])
				if db.has_key('primality_test'):
					self.set_primality_test(db['primality_test'])
				else:
					self.set_primality_test(MillerRabinTest())
				if db.has_key('factorization_method'):
					self.set_factorization_method(db['factorization_method'])
				else:
					self.set_factorization_method(PMinusOneAndExponentMethod())
		db.close()

	def update(self):
		db = shelve.open(self.settings_store)
		db['synchronized'] = False

		db['prime_size'] = self.get_prime_size()
		db['max_iteration_count'] = self.get_iteration_count()
		db['primality_test'] = self.get_primality_test()
		db['factorization_method'] = self.get_factorization_method()

		db['synchronized'] = True
		db.close()

	def is_strong_prime_generator(self):
		return NumberFactorySingleton.get_instance().get_prime_generator().is_strong()

	def set_strong_prime_generator(self):
		if not self.is_strong_prime_generator():
			test = NumberFactorySingleton.get_instance().get_primality_test()
			generator = StrongPrimeGenerator(test)
			NumberFactorySingleton.get_instance().set_prime_generator(generator)
		self.notifica()
		
	def set_simple_prime_generator(self):
		if self.is_strong_prime_generator():
			test = NumberFactorySingleton.get_instance().get_primality_test()
			generator = PrimeGenerator(test)
			NumberFactorySingleton.get_instance().set_prime_generator(generator)
		self.notifica()

	def add_listener(self, l):
		self.listeners.append(l)

	def notifica(self):
		for listener in self.listeners:
			listener.notifica(self)