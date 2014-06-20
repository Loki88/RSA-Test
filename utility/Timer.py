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