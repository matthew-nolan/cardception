import board as b
import list as l
import card as c


class Project(object):

	def __init__(self, name):
		self.name = name
		self.boards = []
		# self.cards = []
		self.description = ""
		self.start_date = ""
		self.end_date = ""
		self.prefix = self.name[0:3].upper()

	def addBoard(self, board_name):
		self.boards.append(b.Board(board_name))
		return None

	def getListOfBoardNames(self):
		ret = []
		for board in self.boards:
			ret.append(board.name)
		return ret


	def getDocument(self):

		document = {
		"name": self.name,
		"boards": self.boards,
		"description": self.description,
		"prefix": self.prefix
		}

		return document
