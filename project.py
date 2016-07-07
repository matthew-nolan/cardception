import board as b
import list as l
import card as c
# from pymongo import MongoClient


class Project(object):

	def __init__(self, name):
		self.name = name
		self.boards = []
		self.cards = []
		self.description = ""
		self.prefix = self.name[0:3].upper()

	def addBoard(self, board_name):
		self.boards.append(b.Board(board_name))
		return None

	def getListOfBoardNames(self):
		ret = []
		for board in self.boards:
			ret.append(board.name)
		return ret


# client = MongoClient()
