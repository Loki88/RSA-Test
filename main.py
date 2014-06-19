#!/usr/bin/env python

__author__      = "Lorenzo Di Giuseppe"
__copyright__   = "Copyright 2014"

from ui.Window import *
from ui.Menu import MenuBox
from ui.Window import MainWindow
from controllers import SettingsControllerSingleton

menu = MenuBox()
SettingsControllerSingleton.get_instance()
MainWindow.get_instance().set_content(menu)
MainWindow.get_instance().main()