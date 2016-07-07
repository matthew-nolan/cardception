import list
import card


class Board(object):

	def __init__(self, name):
		self.name = name
		self.lists = []
		self.description = "Add a description..."

	def addList(self, list_name):
		self.lists.append(list_name)

	def addDescription(self, description):
		self.description = description

	def getListIndex(self, list_name):
		ret = 0
		for i in range(len(self.lists)):
			if self.lists[i] == list_name:
				ret = i
		return ret
