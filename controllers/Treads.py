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

class ThreadManager():

	_instance = None

	def __init__(self):
		self.current_thread = None

	@classmethod
	def get_instance(cls):
		if cls._instance == None:
			cls._instance = NumberFactorySingleton()

		return cls._instance

	def set_current(self, thread):
		self.current_thread = thread

	def stop(self):
		self.current_thread.cancel()