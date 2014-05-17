#!/usr/bin/env python

__author__      = "Lorenzo Di Giuseppe"
__copyright__   = "Copyright 2014"

from random import randint

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

class AKSPrimeTest(SimplePrimeTest):

	def expand(self, num):
		ex = [1]
		i = 0
		while i < num:
		    ex.append(ex[-1] * -(num-i) / (i+1))
		return ex[::-1]

	def is_prime(self, num):
		if num < 2:
			return False
		ex = self.expand(num)
		ex[0] += 1
		return not any(mult % num for mult in ex[0:-1])

class FermatTest(SimplePrimeTest):

	def is_prime(self, num):
		test = pow(2,num-1,num)
		return test == 1

class MillerRabinTest(SimplePrimeTest):

	def is_prime(self, num):
		print("MillerRabinTest for "+str(num))
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
		print("k: "+str(k)+" - m: "+str(m))

		# generazione intero casuale a
		if num-2 > 2:
			a = randint(2,num-2)
		else:
			a = 2
		b0 = pow(a, m, num)
		print("value test: "+str(a)+" value b: "+str(b0))

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