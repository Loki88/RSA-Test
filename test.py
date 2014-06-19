from utility.Math import legendre
from models.NumberGenerator import PrimeGenerator
from models.PrimalityTest import MillerRabinTest

generator = PrimeGenerator(MillerRabinTest())

prime = generator.generate(min=128)

for k in range(prime):
	print("legendre call on "+str(k)+" mod("+str(prime)+"): "+str(legendre(k, prime)))
