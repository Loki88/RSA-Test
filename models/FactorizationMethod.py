from utility.Math import gcd, legendre
from models import SettingsSingleton
from random import randint
from math import sqrt

class FactorizationMethod():

	def __init__(self):
		self.prime_1 = None
		self.prime_2 = None

	def attack(self, client):
		self.mod, self.key = client.get_public_key()
		self.prime_1, self.prime_2 = None, None

	def get_factors(self):
		return (self.prime_1, self.prime_2)

	def is_successful(self):
		return self.prime_1 != None and self.prime_2 != None

class QuadraticSieveMethod(FactorizationMethod):

	def __init__(self):
		FactorizationMethod.__init__(self)

	def attack(self, client):
		FactorizationMethod.attack(self, client)

		k = randint(1,self.mod)

		self.n_part = int(sqrt(self.mod))

		factor_base = []
		i = 0
		while i < k:
			if self.is_residuo(k) == 1:
				factor_base.append(k)
			i += 1
		print(factor_base)


	def is_residuo(self, x):
		return (x + self.n_part)**2 % self.mod == 1


class PMinusOneAndExponentMethod(FactorizationMethod):

	max_iteration_lenght = None

	def __init__(self):
		FactorizationMethod.__init__(self)
		self.count = 0
		self.max_iteration_lenght = SettingsSingleton.get_instance().get_iteration_count()

	def attack(self, client):
		FactorizationMethod.attack(self, client)
		self.count = 0
		length = len(str(bin(self.mod)))
		B = randint(1,5)*length
		self.p_minus_one_factorization(B)

	def p_minus_one_factorization(self, B):
		self.count += 1
		a = 2
		self.B_fact = 1
		b = self.elevate(a, B)

		d = gcd(b-1, self.mod)
		if d > 1 and d < self.mod:
			self.prime_1 = d
			self.prime_2 = self.mod / d
		elif d == self.mod:
			self.global_exponent_factorization(a)
		elif self.count <= self.max_iteration_lenght:
			self.p_minus_one_factorization(B*(self.count*2))


	def global_exponent_factorization(self, a):
		B_fact = self.B_fact
		r = 0
		while B_fact % 2 == 0:
			B_fact = B_fact / 2
			r += 1

		print("r-factor in global exponent method is: "+str(r))

		b0 = pow(a, B_fact, self.mod)
		if b0 != 1:
			while r > 0:
				print("exponent test iteration "+str(r))
				b1 = b0 * b0 % self.mod
				r -= 1
				if b1 == self.mod - 1:
					break
				elif b1 == 1 and (b0 != 1 or b0 != self.mod - 1):
					self.prime_1 = gcd(b0-1, self.mod)
					self.prime_2 = self.mod / self.prime_1
					break
				else:
					b0 = b1


	def elevate(self, a, B):
		# if B > pow(2, 20):
		# 	raise Exception("Maximum recursion exceded, this method works well with small prime factors")
		k = 2
		b = a
		while k <= B:
			self.B_fact *= k
			b = pow(b, k, self.mod)
			k += 1

		return b