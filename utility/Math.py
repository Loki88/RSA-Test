from math import *
from itertools import *
import operator

def __init__(self):
	pass

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

# class Powers():

# 	_instance = None
# 	tartaglia_lines = []
# 	max_lines = 100

# 	def __init__(self):
# 		pass

# 	@classmethod
# 	def get_instance(cls):
# 		if cls._instance == None:
# 			cls._instance = Powers()

# 		return cls._instance

# 	def poly_power(self, a, b, n, mod = None, poly_mod = None):
# 		p = poly_power_tartaglia(a, b, self.get_line_n(n), mod)
# 		if poly_mod != None:
# 			p = self.poly_divide(p, poly_mod)
# 		return p

# 	def get_line_n(self, n):
# 		ran = len(self.tartaglia_lines)
# 		l = int(ran / 2)
# 		while ran > 1:
# 			line = self.tartaglia_lines[l]
# 			if len(line) == n+1:
# 				return line
# 			else:
# 				ran = int(ran / 2)
# 				if len(line) > n+1:
# 					l -= ran
# 				else:
# 					l += ran
		
# 		if len(line) < n + 1:
# 			i = n - len(line) + 1

# 			for j in range(i):
# 				line = tartaglia_next_line(line)
# 		else:
# 			i = len(line) - n - 1

# 			for j in range(i):
# 				line = tartaglia_previous_line(line)

# 		if len(self.tartaglia_lines >= self.max_lines):
# 			self.tartaglia_lines[l] = line
# 		else:
# 			self.tartaglia_lines.insert(l, line)



# def poly_divide(self, poly, max_exp):
# 	deg = len(poly)-1
# 	mid = deg - max_exp
# 	if mid <= 0:
# 		return poly
# 	else:
# 		result = poly[mid:]
# 		i = 0
# 		while i < mid:
# 			result[len(result)-1-i] += poly[i]
# 		return result


# def multiply_poly(pol1, pol2, mod):
# 	i = 0
# 	c_len = len(pol1)
# 	p_len = len(pol2)
# 	result = [0 for i in range(0, c_len + p_len - 1)]
# 	while i < c_len:
# 		while j < p_len:
# 			result[j+i] += pol1[i]*pol2[j] % mod
# 	return result


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

def is_pure_power(n):
    d=int(log(n,2))
    f=filter(lambda x: long(x[0])**x[1]==n, map(lambda x: (n**(1/float(x)),x), range(2, d+1)))
    return len(f)!=0

def poly_quard(P,n,r):
    M=map(lambda (x,y): ((x[0]+y[0])%r,(x[1]*y[1])%n), product(zip(range(r),P),repeat=2))
    P=[0]*r
    for (k,a) in M:
        P[k]+=a
    P=map(lambda x:x%n,P)
    return P

def poly_mul(P1,P2,n,r):
    M=map(lambda (x,y): ((x[0]+y[0])%r,(x[1]*y[1])%n), product(zip(range(r),P1),zip(range(r),P2)))
    P=[0]*r
    for (k,a) in M:
        P[k]+=a
    P=map(lambda x:x%n,P)
    return P

def poly_power(a,n,r):
    #(X+a)^n (mod n, X^r-1)
    #11 --> 1011
    logn=int(log(n,2))+1
    poly_base=[0]*logn
    P0=[0]*r
    PU=[0]*r
    PU[0]=1
    P0[0],P0[1]=a,1
    
    for k in range(logn):
        poly_base[k]=P0
        P0=poly_quard(P0,n,r)
    mask_base=[0]*logn
    tn=n
    for k in range(logn):
        if tn%2==1:
            tn=(tn-1)/2
            mask_base[k]=1
        else:
            tn=tn/2
    FPL=filter(lambda x:x[0]==1,zip(mask_base,poly_base))
    return reduce(lambda P1,P2:poly_mul(P1,P2[1],n,r), FPL, PU)