from models.NumberFactory import NumberFactorySingleton

class PrimeGenerator():

	_instance = None

	@classmethod
	def get_instance(cls):
		if cls._instance == None:
			cls._instance = PrimeGenerator()

		return cls._instance


	def generate(self, size):
		primes = []
		last_primes = 2
		while last_primes <= size:
			primes.append(last_primes)
			last_primes = NumberFactorySingleton.get_instance().get_prime(last_primes).get_value()

		return primes