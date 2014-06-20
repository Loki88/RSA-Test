#!/usr/bin/env python

__author__      = "Lorenzo Di Giuseppe"
__copyright__   = "Copyright 2014"

from random import randint
from .Settings import SettingsSingleton
from threading import Timer
import math
import itertools as IT
import numpy as NP
import fractions
import time

class PrimeTest():

	deterministic = False

	max_time = 1.5

	def is_prime(self, num):
		pass

	def is_deterministic(self):
		return self.deterministic

	def get_timeout(self):
		return self.max_time

class SimplePrimeTest(PrimeTest):

	deterministic = True

	def is_prime(self, num):
		if num % 2 == 0:
			return False

		max = int(sqrt(num))
		i = 3
		while i <= max:
			if num % i == 0:
				timer.cancel()
				return False
			i += 2
		return True


class AKSPrimeTest(PrimeTest):

	deterministic = True
	max_time = 3

	def ordr(self, r, n):
	    for k in IT.count(3):
	        if pow(n, k, r) == 1:
	            return k
             
	def isqrt(self, x):
	    if x < 0:
	        raise ValueError('square root not defined for negative numbers')
	    n = int(x)
	    if n == 0:
	        return 0
	    a, b = divmod(n.bit_length(), 2)
	    x = 2 ** (a + b)
	    while True:
	        y = (x + n // x) // 2
	        if y >= x:
	            return x
	        x = y
         
	def mmultn(self, a, b, r, n):
	    """ Dividing by X^r - 1 is equivalent to shifting the amplitude from
	        position k to k - r
	        a and b are vectors of length r maximum
	        convolve them (equivalent to polynomial mult) and add all amplitudes
	        with exp k of r and higher to exp k - r
	        After the multiplication all amplitudes are taken %n
	    """
	    res = NP.zeros(2 * r, dtype=NP.int64)
	    res[:len(a)+len(b)-1] = NP.convolve(a, b)
	    res = res[:-r] + res[-r:]
	    return res % n
 
	def powmodn(self, pn, n, r, m):
	    res = [1]
	    while n:
	        if n & 1:
	            res = self.mmultn(res, pn, r, m)
	        n //= 2
	        if n:
	            pn = self.mmultn(pn, pn, r, m)
	    return res
 
	def testan(self, a, n, r):
	    pp = self.powmodn([a, 1], n, r, n)
	    pp[n%r] = (pp[n%r] - 1 ) % n # subtract X^n
	    pp[0] = (pp[0] - a) % n      # subtract a
	    return not any(pp)
      
	def phi(self, n):
	    return sum(fractions.gcd(i, n) == 1 for i in range(1, n))
         
	def is_prime(self, n):
		if n == 2:
			return True
		if n < 2:
			return False
		for a in range(2, self.isqrt(n) + 1):
			for b in range(2, n):
				t = a ** b
				if t == n:
					return False
				if t > n:
					break
		logn = math.log(n,2)
		logn2 = logn ** 2
		for r in IT.count(3):
			if fractions.gcd(r, n) == 1 and self.ordr(r, n) >= logn2:
				break
		for a in range(2, r + 1):
			if 1 < fractions.gcd(a, n) < n:
				return False
		if n <= r:
			return True
		for a in range(1, int(math.sqrt(self.phi(r)) * logn)):
			if not self.testan(a, n, r):
				return False
		return True


class MillerTest(PrimeTest):

	deterministic = True

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

class LucasLehmer(PrimeTest):

	deterministic = False

	def is_prime(self, p):
		if p == 2: 
			return True # Lucas-Lehmer test only works on odd primes
		elif p <= 1 or p % 2 == 0:
  			return False
		else:
			for i in range(3, int(sqrt(p))+1, 2 ):
				if p % i == 0: 
					return False
			return True

class FermatTest(PrimeTest):

	deterministic = False

	def is_prime(self, num):
		if num % 2 == 0:
			return False
		else:
			test = pow(2,num-1,num)
			return test == 1

class MillerRabinTest(PrimeTest):

	deterministic = False

	def __init__(self):
		self.max_iter = SettingsSingleton.get_instance().get_iteration_count()

	def is_prime(self, num):
		prime = True
		i = 0
		while i < self.max_iter:
			if not self.test(num):
				return False
			i += 1
		return True

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

		b0 = pow(a, int(m), num)

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