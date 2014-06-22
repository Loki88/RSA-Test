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

from multiprocessing import Process, TimeoutError
import time

class Timer(Process):

	def __init__(self, time, callback, *args, **kwargs):
		Process.__init__(self, target=self.time_wait, args=args, kwargs=kwargs)
		self._callback = callback
		self._time = time
		self._args = args
		self._kwargs = kwargs

	def start(self):
		Process.start(self)

	def time_wait(self):
		i = 0
		while i < self._time:
			time.sleep(1)
			i += 1
		raise TimeoutError()

	def cancel(self):
		self.stop()

	def reset(self):
		self.cancel()
		self.start()