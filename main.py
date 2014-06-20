#!/usr/bin/env python

__author__      = "Lorenzo Di Giuseppe"
__copyright__   = "Copyright 2014"

from ui.Window import *
from ui.Menu import MenuBox
from ui.Window import MainWindow
from controllers import SettingsControllerSingleton
# from models.PrimalityTest import AKSPrimeTest

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