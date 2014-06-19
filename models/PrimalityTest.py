#!/usr/bin/env python

__author__      = "Lorenzo Di Giuseppe"
__copyright__   = "Copyright 2014"

from random import randint
from math import sqrt, log, ceil
from utility.Math import gcd


class SimplePrimeTest():

	def is_prime(self, num):
		if num % 2 == 0:
			return False

		max = int(sqrt(num))
		i = 3
		while i <= max:
			if num % i == 0:
				return False
			i += 2
		return True

	def is_deterministic(self):
		return self.deterministic


class AKSPrimeTest(SimplePrimeTest):

	deterministic = True

	def __init__(self):
		self.speedup = FermatTest()
		self.max = pow(2,15)

	def expand_x_1(self, p):
		ex = [1]
		
		for i in range(p):
			ex.append(ex[-1] * -(p-i) / (i+1))
		print(ex)
		return ex[::-1]

	def is_prime(self, num):
		if num > self.max:
			raise MemoryError("The number is too big for this version of AKS test.")
		if num < 2:
			return False
		if not self.speedup.is_prime(num):
			return False
		ex = self.expand_x_1(num)
		print(ex)
		ex[0] += 1

		return not any(mult % num for mult in ex[0:-1])


class MillerTest(SimplePrimeTest):
	deterministic = True

	def __init__(self):
		pass

	def get_range(self, inf, num):
		return range(1, inf)

	def is_prime(self, num):
		if num == 2:
			return True
		elif num <= 1 or num % 2 == 0:
			return False
		
		d = num -1
		s = 0
		while d % 2 == 0:
			s += 1
			d = d / 2

		ln2 = int(2*(log(num)**2))
		inf = num -1
		if ln2 < inf:
			inf = ln2
		a = 2
		ran = self.get_range(inf, num)
		for a in ran:
			p1 = pow(a, d, num)
			if p1 != 1:
				for r in range(0,s):
					p2 = pow(a, pow(2,r)*d, num)
					if p2 != num-1:
						return False
		return True

class LucasLehmer(SimplePrimeTest):

	def is_prime(self, p):
		if p == 2: return True # Lucas-Lehmer test only works on odd primes
  		elif p <= 1 or p % 2 == 0: return False
  		else:
			for i in range(3, int(sqrt(p))+1, 2 ):
				if p % i == 0: return False
			return True


class FermatTest(SimplePrimeTest):

	deterministic = False

	def is_prime(self, num):
		if num % 2 == 0:
			return false
		else:
			test = pow(2,num-1,num)
			return test == 1



class MillerRabinTest(SimplePrimeTest):

	deterministic = False

	def __init__(self):
		SettingsControllerSingleton

	def is_prime(self, num):
		prime = True
		for 
		if self.test

	def test(self, num):
		if num == 2:
			return True
		if num % 2 == 0:
			return False

		k = 1
		m = (num-1) / 2
		while m % 2 == 0:
			m = m / 2
			k = k + 1

		self.k = k

		# generazione intero casuale a
		if num-2 > 2:
			a = randint(2,num-2)
		else:
			a = 2
		b0 = pow(a, m, num)

		if b0 == 1 or b0 == num-1 or b0 == -1:
			return True
		else:
			return self.make_test(b0, num)

	def make_test(self, b, n):
		b1 = pow(b,2,n)

		if b1 == 1:
			return False
		elif b1 == n-1 or b1 == -1:
			return True
		else:
			if self.k > 0:
				self.k = self.k - 1
				return self.make_test(b1, n)
			else:
				return False