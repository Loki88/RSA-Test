#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2014  Lorenzo Di Giuseppe

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

__author__      = "Lorenzo Di Giuseppe"
__copyright__   = "Copyright 2014"

from utility.Math import gcd, legendre
from models import SettingsSingleton
from random import randint
from cmath import phase
import numpy as np
from decimal import *
from math import sqrt
from multiprocessing import Pool
from .PrimalityTest import AKSPrimeTest, MillerRabinTest
from utility.Math import continued_fraction_next_step, continued_fraction, smart_int_divide, smart_int_pow, smart_2_decomposition
import time


mtest = MillerRabinTest()
n_primes = [2]
i = 1
n = 3
while i <= 100:
	if mtest.is_prime(n):
		n_primes.append(n)
		i += 1
	n += 2



class FactorizationMethod():
	'''
	Base class for factorization methods.
	'''

	def __init__(self):
		self.prime_1 = None
		self.prime_2 = None

	def attack(self, client):
		'''
		Base method. When this method is called with an instance of RSAClient
		'''
		self.mod, self.key = client.get_public_key()
		self.prime_1, self.prime_2 = None, None

	def get_factors(self):
		return (self.prime_1, self.prime_2)

	def is_successful(self):
		return self.prime_1 != None and self.prime_2 != None and self.prime_1 != 1 \
			and self.prime_2 != 1 and self.prime_1 != self.mod and self.prime_2 != self.mod
		# and self.prime_1 != 1 and self.prime_2 != 1

	def is_on_mod(self):
		return True

class QuadraticSieveMethod(FactorizationMethod):

	base_size = 100
	primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 33, 37]
	randomizer = 1

	def __init__(self):
		FactorizationMethod.__init__(self)
		self.max_iteration_lenght = SettingsSingleton.get_instance().get_iteration_count()
		self.count = 0
		if self.base_size < len(n_primes):
			self.primes = n_primes[:self.base_size]
		else:
			self.primes = n_primes

		self.base_size = len(self.primes)
		# i = 
		# test = MillerRabinTest()
		# self.primes = [2]
		# prime_timeout = test.get_timeout()
		# start = 3
		# with Pool(processes=1) as pool:
		# 	while len(self.primes) < self.base_size:
		# 		res = pool.apply_async(test.is_prime, args=(start,))
		# 		result = res.get(timeout=prime_timeout)
		# 		res.wait()
		# 		if result:
		# 			self.primes.append(start)
		# 		start += 2

	def attack(self, client):
		FactorizationMethod.attack(self, client)
		for i in range(self.max_iteration_lenght):
			print("Trying for the "+str(i)+" time")
			self.factorize()
			if self.is_successful():
				return
			self.randomizer *= 1.2

	def factorize(self):
		bad_squares = 0
		k = randint(1,self.mod)
		self.n_part = sqrt(self.mod)
		self.squares = []
		self.squares_set = set()
		self.factor_base = []
		i = 1
		with localcontext() as ctx:
			ctx.prec = 10
			while len(self.factor_base) <= 2*self.base_size:
				i = randint(1, 10)*(self.randomizer)
				for j in range(20):
					b = int(i*self.n_part+j)
					quad = pow(b,2,self.mod)
					fact = []
					for p in self.primes:
						fact.append(0)
						while quad % p == 0:
							fact[-1] += 1
							quad = quad / p

					if quad == 1 and not b in self.squares_set:
						self.squares_set.add(b)
						self.squares.append(b)
						self.factor_base.append(fact)
					"""
					Else our primes are too small to give a correct factorization.
					Choose another number.
					"""
				self.randomizer += 0.1
		self.find_squares()

	def find_squares(self):
		matrix = np.asarray(self.factor_base).__mod__(2)
		"""
		If a column contains only one 1, the row associated
		cannot be part of a square. Remove it!
		"""
		matrix = self.reduce(matrix)
		"""
		Base version, iterate on matrices of growing size.
		Rows contains relations of 1, 2, 3 and so on.
		"""
		relations = self.find_relations(matrix)
		for relation in relations:
			if self.is_valid_relation(relation):
				return


	def is_valid_relation(self, rows):
		if len(rows) < 2:
			return False
		a = 1
		b = 1
		for i in rows:
			a *= self.squares[i] % self.mod
			for k in range(len(self.primes)):
				b *= pow(self.primes[k], int(self.factor_base[i][k] / 2), self.mod)

		if (a - b) % self.mod == 0 or (a + b) % self.mod == 0:
			return False
		else:
			prime_1 = gcd(a - b, self.mod)
			if prime_1 == 1:
				prime_1 = gcd(a+b, self.mod)
			if prime_1 != 1:
				self.prime_1 = prime_1
				self.prime_2 = self.mod / self.prime_1
				return True
			return False


	def reduce(self, matrix):
		for i in range(len(matrix[0])):
			if matrix[:,i].sum() == 1:
				row = len(matrix)
				k = 0
				while k < row:
					if matrix[k, i] == 1:
						matrix = np.delete(matrix, (k), axis=0)
						row = len(matrix)
					k += 1
		return matrix

	def find_relations(self, matrix):
		relations = []
		row = len(matrix)
		col = len(matrix[0])
		col_ones = []
		row_ones = []
		for i in range(row):
			row_ones.append(matrix[i].sum())
		for i in range(col):
			col_ones.append(matrix[:,i].sum())

		for i in range(row):
			row_weight = row_ones[i]
			if row_weight == 0:
				continue
			current_row = matrix[i]
			candidate_rows = []
			for j in range(row):
				if i!=j and row_ones[j] <= row_weight:
					candidate_rows.append(j)
			combination = [i]
			for j in candidate_rows:
				new_weight = current_row.__xor__(matrix[j]).sum()
				if new_weight < row_weight:
					combination.append(j)
					current_row = current_row.__xor__(matrix[j])
					row_weight = new_weight
					candidate_rows.remove(j)
			if row_weight == 0:
				relations.append(combination)

		return relations


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
		B_fact, r = smart_2_decomposition(self.B_fact)
		if r == 0:
			return
		try:
			b0 = pow(a, B_fact, self.mod)
		except:
			b0 = smart_int_pow(a, B_fact, self.mod)
		if b0 != 1:
			while r > 0:
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
		k = 2
		b = a
		while k <= B:
			self.B_fact *= k
			b = pow(b, k, self.mod)
			k += 1

		return b


class LowExponentAttack(FactorizationMethod):

	def attack(self, client):
		FactorizationMethod.attack(self, client)
		'''
		C è candidato ad essere theta di eulero
		'''
		prec = 40
		rounding = 0.1
		with localcontext() as ctx:
			ctx.prec = prec
			e = Decimal(self.key)
			n = Decimal(self.mod)
			x, a, p, q = continued_fraction_next_step(self.key/self.mod,ctx,first=True)
			i = 0
			while i < prec+1:
				x, a, p, q = continued_fraction_next_step(x,a,p,q,ctx)
				if p[0] != 0:
					C = (e * q[0] - 1) / p[0]
					if C - int(C) < rounding or int(C) + 1 - C < rounding:
						self.solve(int(C), rounding)
						if self.is_successful():
							break
				x, a, p, q = continued_fraction_next_step(x,a,p,q,ctx)
				i += 2

	def solve(self, theta, rounding):
		p = [1, -self.mod + theta - 1, self.mod]
		primes = np.roots(p)
		try:
			prime_1 = int(primes[0])
			prime_2 = int(primes[1])
			if prime_1 == primes[0] and prime_2 == primes[1]:
				self.prime_1 = prime_1
				self.prime_2 = prime_2
				return

			if abs(primes[0] - prime_1) < rounding:
				if self.mod % prime_1 == 0:
					self.prime_1 = prime_1
					self.prime_2 = self.mod / prime_1
					return

			if  abs(primes[1] - prime_2) < rounding:
				if self.mod % prime_2 == 0:
					self.prime_1 = self.mod / prime_2
					self.prime_2 = prime_2
		except:
			pass

	def is_on_mod(self):
		return False

		