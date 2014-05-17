from models.NumberFactory import NumberFactorySingleton
from models.FactorizationMethod import PMinusOneAndExponentMethod

class SettingsControllerSingleton():

	_instance = None

	@classmethod
	def get_instance(cls):
		if cls._instance == None:
			cls._instance = SettingsControllerSingleton()

		return cls._instance


	def get_primality_test(self):
		test = NumberFactorySingleton.get_instance().get_primality_test()
		return test

	def get_factorization_method(self):
		return PMinusOneAndExponentMethod()

	def set_primality_test(self, test):
		new_test = test()
		print("test "+new_test.__class__.__name__)
		NumberFactorySingleton.get_instance().set_primality_test(test())

	def set_factorization_method(self, method):
		pass