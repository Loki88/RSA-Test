#!/usr/bin/env python

__author__      = "Lorenzo Di Giuseppe"
__copyright__   = "Copyright 2014"

from utility.Math import gcd, legendre
from models import SettingsSingleton
from random import randint
import numpy as np
from decimal import *
from math import sqrt
from multiprocessing import Pool
from .PrimalityTest import AKSPrimeTest
from utility.Math import continued_fraction_next_step, continued_fraction
import time

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
		return self.prime_1 != None and self.prime_2 != None 
		# and self.prime_1 != 1 and self.prime_2 != 1

class QuadraticSieveMethod(FactorizationMethod):

	primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 33, 37]
	randomizer = 1

	def __init__(self):
		FactorizationMethod.__init__(self)
		self.max_iteration_lenght = SettingsSingleton.get_instance().get_iteration_count()
		self.count = 0
		base_size = 40
		i = 0
		test = AKSPrimeTest()
		self.primes = [2]
		prime_timeout = test.get_timeout()
		start = 3
		with Pool(processes=1) as pool:
			while len(self.primes) < base_size:
				res = pool.apply_async(test.is_prime, args=(start,))
				result = res.get(timeout=prime_timeout)
				res.wait()
				if result:
					self.primes.append(start)
				start += 2

	def attack(self, client):
		FactorizationMethod.attack(self, client)
		self.factorize()
		self.count = 0

	def factorize(self):
		k = randint(1,self.mod)
		self.count += 1
		if self.count > self.max_iteration_lenght:
			return
		self.n_part = sqrt(self.mod)
		self.squares = []
		self.factor_base = []
		j = randint(1, 9)*self.randomizer
		while True:
			for i in range(1,9):
				b = int(sqrt(i)*self.n_part+j)
				quad = b**b % self.mod
				fact = []
				for p in self.primes:
					fact.append(0)
					while quad % p == 0:
						fact[-1] += 1
						quad = quad / p

				if quad == 1:
					self.squares.append(b)
					self.factor_base.append(fact)
					break
				"""
				Else our primes are too small to give a correct factorization.
				Choose another number.
				"""
			if len(self.factor_base) > len(self.primes):
				break
			j += 1

		self.find_squares()


	def find_squares(self):
		matrix = np.asarray(self.factor_base).__mod__(2)
		print(matrix, "Factor base")
		"""
		If a column contains only one 1, the row associated
		cannot be part of a square. Remove it!
		"""
		matrix = self.reduce(matrix)
		print(matrix, "Reduced matrix")
		"""
		Base version, iterate on matrices of growing size.
		Rows contains relations of 1, 2, 3 and so on.
		"""
		relations = self.find_relations(matrix)
		for relation in relations:
			if self.is_valid_relation(relation):
				return
		self.randomizer +=1
		self.factorize()


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
			print((a-b)%self.mod, "Resto a-b")
			print((a+b)%self.mod, "Resto a+b")
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
		print(row_ones, "Row ones")
		print(col_ones, "Col ones")
		for i in range(row):
			row_weight = row_ones[i]
			if row_weight == 0:
				continue
			current_row = matrix[i]
			
			print(current_row, "Finding combination with this row with weight <= "+str(row_weight))
			candidate_rows = []
			for j in range(row):
				if i!=j and row_ones[j] <= row_weight:
					candidate_rows.append(j)
			print(candidate_rows, "Candidates are")
			combination = [i]
			# rows_candidate = len(candidate_rows)
			# while row_weight > 0 and rows_candidate > 0:
			for j in candidate_rows:
				new_weight = current_row.__xor__(matrix[j]).sum()
				if new_weight < row_weight:
					combination.append(j)
					current_row = current_row.__xor__(matrix[j])
					row_weight = new_weight
					candidate_rows.remove(j)
						# rows_candidate -= 1
			if row_weight == 0:
				relations.append(combination)
				print(current_row, "Azzerando")
				print(combination, "Combinazione")
			else:
				print(combination, "not good")

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
		B_fact = self.B_fact
		r = 0
		while B_fact % 2 == 0:
			B_fact = long(B_fact) / 2
			r += 1
		B_fact = B_fact % (self.mod-1)
		b0 = pow(a, B_fact, self.mod)
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
		# if B > pow(2, 20):
		# 	raise Exception("Maximum recursion exceded, this method works well with small prime factors")
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
		print(self.key / self.mod, "Num")
		'''
		C e candidato ad essere theta di eulero
		'''
		i = 1
		while True:
			p, q = continued_fraction(Decimal(self.key / self.mod), i)
			print(p/q, "Fraction gives")
			if p != 0:
				C = (self.key * q - 1) / p
				if C % 1 == 0:
					self.solve(C)
					if self.is_successful():
						break
			i += 1

	def solve(self, theta):
		p = [1, -(self.mod - theta + 1), self.mod]
		primes = np.roots(p)
		print(primes, "Primes attacked")
		if int(primes[0]) == primes[0] and int(primes[1]) == primes[1]:
			self.prime_1 = primes[0]
			self.prime_2 = primes[1]

		