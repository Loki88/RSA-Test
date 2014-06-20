from itertools import *
from math import *
import operator

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
	if num1 > num2:
		b = num1
		a = num2
	else:
		b = num2
		a = num1

	while a != 0 :
		a, b = b % a, a

	return b

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