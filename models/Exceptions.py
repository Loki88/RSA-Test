from threading import ThreadError
import thread

class Timeout(ThreadError):

	def __init__(self):
		thread.exit()

	def __str__(self):
		return "This operation is taking too much time. Check application settings."
