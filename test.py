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

from utility.Math import legendre
from models.NumberGenerator import PrimeGenerator
from models.PrimalityTest import MillerRabinTest

generator = PrimeGenerator(MillerRabinTest())

prime = generator.generate(min=128)

for k in range(prime):
	print("legendre call on "+str(k)+" mod("+str(prime)+"): "+str(legendre(k, prime)))
