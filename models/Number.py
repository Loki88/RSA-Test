from utility.Math import gcd

class Number():

	def __init__(self, generator, **kwargs):
		self.generator = generator
		self.generate(**kwargs)

	def generate(self, **kwargs):
		self.value = self.generator.generate(**kwargs)

	def get_value(self):
		return self.value

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
		prime = False
		while not self.test.is_prime(start):
			start += 2

		return start

	def set_test(self, test):
		self.test = test

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