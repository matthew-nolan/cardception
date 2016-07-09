import board
import card
import separator

class List(object):

	def __init__(self, name):
		self.name = name
		self.board_name = ""
		# a list of cards or separatators
		self.items = []

	def getDocument(self):
		document = {
			"name": self.name,
			"items": self.items
		}

		return document

	def addCard(self, card):
		self.items.append(card)

	def addSeparator(self, separator):
		self.items.append(separator)

	def moveItem(self, from_index, to_index):
		item_being_moved = self.items.pop(from_index)

		if from_index > to_index:
			self.items.insert(to_index, item_being_moved)
		if from_index < to_index:
			self.items.insert(to_index + 1, item_being_moved)

	def moveItemToTop(self, from_index):
		self.items.insert(0, self.items[from_index])

	def moveItemToBottom(self, from_index):
		self.items.append(self.items.pop(from_index))

	def duplicateItem(self, card_index, to_board, to_list):
		to_list_index = 0

		for i in range(len(to_board.lists)):
			if to_board.lists[i].name == to_list.name:
				to_list_index = i

		to_board.lists[to_list_index].addCard(self.items[card_index])

	def assignAttributeToAll(self, attribute, value):

		for i in range(len(self.items)):
			if type(self.items[i]) == card.Card:
				setattr(self.items[i], attribute, value)
