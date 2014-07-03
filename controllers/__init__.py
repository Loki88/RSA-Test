#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Modulo di controllori. Ogni controllore esegue le operazioni onerose in multiprocessing.
In ogni caso, per evitare freeze nelle interfacce è opportuno eseguire le operazioni dei controllori in thread separati.
'''

__author__      = "Lorenzo Di Giuseppe"
__copyright__   = "Copyright 2014"

from .PrimeGenerator import PrimeGenerator
from .SettingsController import SettingsControllerSingleton
from .SecurityBrokeController import RSAComunicationAttackTest
from .SettingsController import SettingsControllerSingleton
from .Threads import Thread