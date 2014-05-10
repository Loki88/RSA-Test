from ui.Window import *
from ui.Menu import MenuBox
from ui.Window import MainWindow

menu = MenuBox()
MainWindow.get_instance().set_content(menu.get_content())
MainWindow.get_instance().main()