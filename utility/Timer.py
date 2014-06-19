from threading import Timer as T


class Timer():

	def __init__(self, time, callback, *args, **kwargs):
		self._callback = callback
		self._time = time
		self._args = args
		self._kwargs = kwargs

	def start(self):
		self.timer = T(self._time, self._callback)

	def cancel(self):
		self.timer.cancel()