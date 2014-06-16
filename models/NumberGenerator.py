from utility.Math import *

class NumberGenerator():

	def generate(self, **kwargs):
		pass


class PrimeGenerator(NumberGenerator):

	def __init__(self, test):
		self.test = test

	def generate(self, **kwargs):
		min = kwargs['min']
		if min == None:
			min = 1
		start = min + 1
		if start % 2 == 0:
			start += 1
		
		while not self.test.is_prime(start):
			start += 2

		return start

	def set_test(self, test):
		self.test = test

	def get_test(self):
		return self.test

	def is_strong(self):
		return False


class StrongPrimeGenerator(PrimeGenerator):
	'''
	This class is safe from p-1 and small factors attacks
	'''

	size = 20

	def generate(self, **kwargs):
		'''
		Here we need to add the logic to prevent that value-1 has small prime factors.
		Look: the test logic is added by StrongPrimeGenerator's father (PrimeGenerator)
		'''
		min = kwargs['min']
		if min == None:
			if self.test.is_deterministic():
				kwargs['min'] = pow(2, 10)
			else:
				kwargs['min'] = pow(2, 20)

		start = PrimeGenerator.generate(self, **kwargs)

		print("Big prime: "+str(start))

		k = 2
		while True:
			p = k*start + 1
			if self.test.is_prime(p):
				break
			else:
				k = k + 1

		print("Strong prime: "+str(p))

		return p

	def is_strong(self):
		return True
		

class CoprimeGenerator(NumberGenerator):

	def generate(self, **kwargs):
		min = kwargs['min']
		max = kwargs['max']
		b = kwargs['num']
		a = 2
		if min != None:
			a = min

		increment = 1
		if b % 2 == 0:
			if a % 2 == 0:
				a += 1
			increment = 2

		while gcd(a,b) != 1:
			a += increment

		if not max == None and a > max:
			return None

		return a