class Euclidean():

	@staticmethod
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

	@staticmethod
	def egcd(a, b):
	    if a == 0:
	        return (b, 0, 1)
	    else:
	        g, y, x = Euclidean.egcd(b % a, a)
	        return (g, x - (b // a) * y, y)

	@staticmethod
	def getCoprime(b, min = None, max = None):
		a = 2
		if min != None:
			a = min

		increment = 1
		if b % 2 == 0:
			if a % 2 == 0:
				a += 1
			increment = 2

		gcd, x, y = Euclidean.egcd(a, b)
		while gcd != 1:
			a += increment
			gcd, x, y = Euclidean.egcd(a, b)

		if not max == None and a > max:
			return None

		return a