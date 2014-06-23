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

from ui.Window import *
from ui.Menu import MenuBox
from ui.Window import MainWindow
from controllers import SettingsControllerSingleton
# from models.PrimalityTest import AKSPrimeTest
# from utility.Math import continued_fraction, continued_fraction_next_step

# pi = 3.14
# x, a, p, q = continued_fraction_next_step(pi)
# print(p[0]/q[0], "Firts expansion [p="+str(p[0])+", q="+str(q[0])+"]")
# x, a, p, q = continued_fraction_next_step(x, a, p, q)
# print(p[0]/q[0], "Second expansion [p="+str(p[0])+", q="+str(q[0])+"]")
# x, a, p, q = continued_fraction_next_step(x, a, p, q)
# print(p[0]/q[0], "Third expansion [p="+str(p[0])+", q="+str(q[0])+"]")

license = '''
RSA & Primality Test  Copyright (C) 2014  Lorenzo Di Giuseppe
This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
This is free software, and you are welcome to redistribute it
under certain conditions; type `show c' for details.
'''

print(license)

menu = MenuBox()
SettingsControllerSingleton.get_instance()
MainWindow.get_instance().set_content(menu)
MainWindow.get_instance().main()

# test = AKSPrimeTest()
# for i in range(70):
# 	print(test.is_prime(i), "Is prime "+str(i)+"?")


# with Pool(processes=1) as pool:
# 	for prime in range(11, 1001, 2):
# 		res = pool.apply_async(test.is_prime, args=(prime,))
# 		try:
# 			result = res.get(timeout=0.001)
# 			if result:
# 				print(prime, "Prime: ")
# 			else:
# 				print(prime, "Not prime")
# 		except Exception as e:
# 			raise MemoryError(e)