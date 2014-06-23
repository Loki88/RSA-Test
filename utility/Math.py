#!/usr/bin/env python

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

from itertools import *
from math import sqrt, log
import operator
from decimal import *

def __init__(self):
	pass

def fast_pow(a,b,mod):
	if b == 1 or a == 1 or a % mod == 1 or a % mod == 0:
		return a
	else:
		if b > mod:
			b = b % mod
		while b % 2 == 0:
			a = a*a % mod
			b /= 2
		return fast_pow(a, b, mod)

def gcd(num1, num2):
	'''
	Calcolo del massimo comun divisore tra due numeri
	'''
	if num1 > num2:
		b = num1
		a = num2
	else:
		b = num2
		a = num1

	while a != 0 :
		a, b = b % a, a

	return b

def smart_2_decomposition(num):
	'''
	Il metodo sfruttando la rappresentazione binaria decompone velocemente un numero intero n in una potenza di 2, k, e un intero m, tali che: n = m*2^k
	'''
	if num < 2:
		return num, 0
	num_bin = str(bin(num)[2:])
	r = 0
	while num_bin[len(num_bin)-1] == "0":
		if len(num_bin) == 2:
			num_bin = num_bin[0]
		else:
			num_bin = num_bin[:-1]
		r += 1
	m = int(str(num_bin), 2)
	return m, r # num = m*2^r

def smart_int_divide(num, div):
	l1 = len(str(num))
	l2 = len(str(div))
	if l1 > l2:
		n1 = pow(10, l1-l2-1)
		n2 = num - div * n1
		return n1 + n2 / div
	else:
		return Decimal(num) / Decimal(div)

def smart_int_pow(num, p, mod):
	if p < 0:
		raise ArithmeticError("Negative exponent")
	num = num % mod
	if p == 1:
		return num
	while p % 2 == 0:
		num = num * num % mod
		p = int(bin(p)[:-2])
	if p > 1:
		num = pow(int(num), int(p), mod)
	print("SMART POW!")
	return num

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def jacobi(a,b):
	pass


def legendre(a,b):
	pass

def is_perfect_power(num):
	log_num = log(num,2)
	inf = int(log_num)
	if log_num == inf:
		return True
	b = 2
	while b < inf:
		low = 2
		high = num
		while high-low > 1:
			mid = low+(high-low)/2
			mid_pow = pow(mid, b)
			if mid_pow < num:
				low = mid
			elif mid_pow > num:
				high = mid
			else:
				return True
		if pow(low, b) == num:
			return True
		b += 1

	return False

def tartaglia_next_line(line_n=None):
	if line_n == None:
		return [1]
	else:
		line_n.insert(0,0)
		line_n.append(0)
		return [line_n[i]+line_n[i+1] for i in range(0, len(line_n)-1)]

def tartaglia_previous_line(line_n):
	l = len(line_n)-1
	previous = [1]
	i = 1
	while i < l:
		previous.append(line_n[i]-previous[i-1])
		i += 1
	return previous

def poly_power_tartaglia(a,b,tartaglia_line, mod=None):
	n = len(tartaglia_line)
	result = []
	if mod == None:
		return [pow(a,n-i-1)*pow(b,i)*tartaglia_line[i] for i in range(0,n)]
	else:
		return [pow(a,n-i-1,mod)*pow(b,i,mod)*tartaglia_line[i] for i in range(0,n)]

def wowrange(start, stop, step=1):
	if step == 0:
		raise ValueError('step must be != 0')
	elif step < 0:
		proceed = operator.gt
	else:
		proceed = operator.lt
	while proceed(start, stop):
		yield start
		start += step

def continued_fraction(n, step=1):
	'''
	Calcolo della frazione continua di n al passo step.
	'''
	a0 = int(n)
	x0 = n
	if a0 == x0:
		return a0, 1
	pn_1, pn_2 = 1, 0
	qn_1, qn_2 = 0, 1
	xn, an = x0, a0
	context = decimal.Context(prec=100)
	for i in range(step):
		pn = an * pn_1 + pn_2
		qn = an * qn_1 + qn_2
		if xn == an:
			'''
			stop
			'''
			return pn, qn
		xn_1 = xn
		an_1 = an
		xn = context.divide(1, (xn_1 - an_1))
		an = int(xn)
		pn_2 = pn_1
		qn_2 = qn_1
		pn_1 = pn
		qn_1 = qn
		
	return pn, qn

def continued_fraction_next_step(n, a=0, p=(1, 0), q=(0, 1), context=None, first=False):
	'''
	Calcolo della frazione continua di n per passi.
	'''
	pn_1, pn_2 = Decimal(p[0]), Decimal(p[1])
	qn_1, qn_2 = Decimal(q[0]), Decimal(q[1])
	n = Decimal(n)
	if first:
		a = int(n)
		return n, a, (a, 1), (1,0)
	xn_1, an_1 = n, a
	xn = Decimal(1) / Decimal(xn_1 - an_1)
	an = int(xn)
	if xn == an:
		return (pn_1, pn_2), (qn_1, qn_2)
	pn = Decimal(an * pn_1 + pn_2)
	qn = Decimal(an * qn_1 + qn_2)
	return xn, an, (pn, pn_1), (qn, qn_1)