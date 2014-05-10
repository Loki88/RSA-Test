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