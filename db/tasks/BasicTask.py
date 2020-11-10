import abc

class BasicTask:
	path_files = 'db/assets/'

	@abc.abstractmethod
	def file_name(self):
		return None

	def full_path(self):
		return self.path_files+self.file_name()

	def get_file(self):
		return open(self.full_path())

