

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